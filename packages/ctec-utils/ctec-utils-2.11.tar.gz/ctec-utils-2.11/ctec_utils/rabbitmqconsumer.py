#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: zhang zi xiao

import signal
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from kombu.connection import Connection
from kombu.entity import Queue
from kombu.mixins import ConsumerMixin
from datetime import datetime
from threading import Condition
import logging


__all__ = ["ConsumerMixinFix", "Consumer", "MessageAckCode", "SUCCESS", "REDELIVER", "REJECT"]

SUCCESS = 0
REDELIVER = 1
REJECT = 2


class MessageAckCode:
    """
    消息应答码
     SUCCESS 执行动作 message.ack()
     REDELIVER 执行动作 message.requeue()
     REJECT或其他未识别的值：message.reject()
    """
    SUCCESS = 0
    REDELIVER = 1
    REJECT = 2


class ConsumerMixinFix(ConsumerMixin):

    _logger = None

    def __init__(self, amqp_url, queues, callback_handle, consumer_tag=None, prefetch_count=10, thread_num=30,
                 heartbeat=45, connect_timeout=15, is_rpc=False, durable=True, logger=None, max_restart_times=3):
        """
        queues 传入队列及其相应的处理函数如:["a.b.a","c.d.c"] 或 "a.b.c"其中msg_handle为对应的回调函数
        :param amqp_url: 队列地址
        :param queues: 队列名
        :param callback_handle: 对应的业务处理方法
        :param consumer_tag: 消费者标识
        :param prefetch_count: 一次拉取的消息数，默认10
        :param thread_num: 线程池线程个数，默认30
        :param heartbeat: 心跳间隔，默认45秒
        :param connect_timeout: 心跳间隔，默认5秒
        :param is_rpc: 是否是RPC服务，默认为False
        :param durable: 是否持久化
        :param logger: 日志输出对象
        :param max_restart_times: 发生connectionerror异常时最大重连次数 默认5次
        """
        if not queues or not callback_handle:
            raise Exception("queues,以及callback_handle回调函数不能为空")

        self._logger = logger if logger else logging.getLogger(__name__)
        self.consumers = list()
        self.amqp_url = amqp_url
        self.heartbeat = heartbeat
        self.connect_timeout = connect_timeout
        self.consumer_tag = consumer_tag
        self.pool = ThreadPoolExecutor(max_workers=thread_num)
        self.prefetch_count = prefetch_count
        self.callback_handle = callback_handle
        self.is_rpc = is_rpc
        self._lock = Condition()
        self.durable = durable
        # 初始化连接
        self.connection = None
        self.re_conn_times = 0
        self.connect_max_retries = max_restart_times if max_restart_times else 1
        self.connection = self.init_connection()
        self.queue = [Queue(queues, durable=self.durable)] if isinstance(queues, str) \
            else [Queue(queue, durable=self.durable) for queue in queues]

    def init_connection(self):
        return Connection(self.amqp_url, heartbeat=self.heartbeat, connect_timeout=self.connect_timeout)

    def get_consumers(self, consumer_cls, channel):
        """
        获取queue对应的消息消费方法
        :param consumer_cls:
        :param channel:
        :return:
        """

        suffix = datetime.now().strftime("%m%d%H%M%S")

        try:
            tag_prefix = "%s_%s_" % (self.consumer_tag, suffix)
            self._logger.debug("consumer=%s get_consumers into current connection id=%s" %
                               (tag_prefix, self.connection.connection._connection_id))
            cbk = partial(self.on_message, queue_name=str(self.queue))
            consumer = consumer_cls(self.queue, callbacks=[cbk],
                                    prefetch_count=self.prefetch_count,
                                    tag_prefix=tag_prefix,
                                    auto_declare=False)
            consumer.qos(prefetch_count=self.prefetch_count)
            self.consumers.append(consumer)

        except Exception as e:
            self._logger.warning("获取连接异常%s" % e)
        return self.consumers

    def on_message(self, body, message, queue_name):
        """
        线程池调用函数
        :param body: 收到的内容
        :param message: 队列收到的对象
         :param queue_name: 队列名
        :return:
        """
        try:
            self._logger.debug("delivery_tag%s,on_message=%s" % (message.delivery_info.get("delivery_tag"), body))
            if not self.connection.connected:
                self.on_connection_revived()
            self.pool.submit(self.message_work, body, message, queue_name)
        except AssertionError as e:
            self._logger.error("on_message body=%s=%s,AssertionError %s" % (body, message, e))
            message.requeue()

    def message_work(self, body, message, queue_name):
        code = MessageAckCode.SUCCESS
        try:
            result = self.callback_handle(body, message)
            if isinstance(result, (tuple, list)):
                code = result[0]
                msg = result[1]
            else:
                code = result
                msg = None
            self._logger.debug('queue_name=%s,delivery_tag%s have been processed. Result code = %s; Result Msg = %s' %
                               (queue_name, message.delivery_info.get("delivery_tag"), code, msg))
        except Exception as e:
            self._logger.error("queue_name%s, message handle error,message_body=%s,error=%s" % (queue_name, body, e))

        try:
            if code is MessageAckCode.SUCCESS:
                message.ack()
            elif code is MessageAckCode.REDELIVER:
                message.requeue()
            elif code is MessageAckCode.REJECT:
                message.reject()
            else:
                message.ack()
        except Exception as e:
            self._logger.error("method message_work ack error,message_body=%s,error=%s" % (body, e))

    def stop(self, sig_number=None, stack_frame=None):
        """
        入参暂时未处理
        :param sig_number: 信号
        :param stack_frame:
        :return:
        """
        self.should_stop = True
        self._logger.error("into stop sig_number=%s, stack_frame=%s" % (sig_number, stack_frame))
        self.close_consumer()
        self.pool.shutdown(wait=True)
        self.release_conn()
        del sig_number, stack_frame

    def release_conn(self):
        self._logger.error("connection released")
        if not self.connection:
            return False
        try:
            self.connection.release()
            return True
        except Exception:
            return False

    def close_consumer(self):
        if not self.consumers:
            return True
        try:
            for consumer in self.consumers:
                consumer.close()
        except Exception as e:
            self._logger.error("close consumer error %s" % e)
            return False
        return True

    def on_connection_revived(self):
        self._logger.warning("connection start revive message")

    def on_connection_error(self, exc=None, interval=None):
        """
        连接失败时业务处理、kumbo会自动重连，这里只为了防止出现connection closed异常将连接释放掉
        :param exc:
        :param interval: 回调回来的自增步长为2
        :return:
        """
        try:
            logging.exception(exc)
            self._logger.error("on_connection_error=%s,interval=%s" % (exc, interval))
            if interval and interval > self.connect_max_retries:
                self.should_stop = True
            #     self.stop(signal.SIGTERM, signal.SIGINT)
            # else:
            #     self.init_connection()
        except Exception as e:
            self._logger.error("连接关闭%s", e)

    def run(self, _tokens=1, timeout=None, **kwargs):
        if not self.callback_handle:
            raise Exception('消息处理回调函数callback_handle不可用!')
        restart_limit = self.restart_limit
        # errors = (self.connection.connection_errors +
        #           self.connection.channel_errors)
        self.re_conn_times = 0
        while not self.should_stop:
            try:
                if restart_limit.can_consume(_tokens):  # pragma: no cover
                    for _ in self.consume(limit=None, **kwargs):
                        pass
                else:
                    sleep(restart_limit.expected_time(_tokens))
            except self.connection.connection_errors as con_e:
                self._logger.error("run rabbitmq consumer error connection_errors:%s" % con_e)
                self.re_conn_times = self.re_conn_times + 1
                self.on_connection_error(con_e, self.re_conn_times)
            except self.connection.channel_errors as ch_e:
                self._logger.error("run rabbitmq consumer error will be stop channel_errors:%s" % ch_e)
                try:
                    if ch_e.code == 404:
                        self.stop(signal.SIGTERM, signal.SIGINT)
                except Exception as es:
                    self._logger.error(" get Exception  code ERROR=%s", es)


class Consumer(ConsumerMixinFix):
    """
    例子：
        def worker(data):
            ...
            :return SUCCESS


        consumer = Consumer("amqp://smallrabbit:123456@172.16.20.73:5672/order", "q.order.tyxb.zfk", worker)
        consumer.run()
    """

    def __init__(self, amqp_url, queues, callback_handle, consumer_tag=None, prefetch_count=10, thread_num=30,
                 heartbeat=45, connect_timeout=15, is_rpc=False, durable=True, logger=None):

        super(Consumer, self).__init__(amqp_url, queues, callback_handle, consumer_tag=consumer_tag,
                                       prefetch_count=prefetch_count, thread_num=thread_num, heartbeat=heartbeat,
                                       connect_timeout=connect_timeout, is_rpc=is_rpc, durable=durable, logger=logger)

    def run(self, _tokens=1, timeout=None, **kwargs):
        """
        启动位置
        :param _tokens: 父类参数默认值
        :param timeout: 单次获取消息最大耗时单位秒（s）
        :param kwargs: 父类参数默认值
        :return:
        """
        assert self.queue is not None
        assert self.callback_handle is not None
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        super(Consumer, self).run(_tokens, timeout, **kwargs)
