# import pika


# class RabbitUtil:
#     """Rabbitmq工具类"""
#     connection = None

#     @classmethod
#     def init(cls, env):
#         try:
#             credential = pika.PlainCredentials(env.username, env.password)
#             cls.connection = pika.BlockingConnection(pika.ConnectionParameters(env.host, env.port, env.vhost, credential, heartbeat=0))
#             queue = env.exchange.replace('ex', 'q')
#             cls.bind_queue_exchange(queue, env.exchange, env.routing_key)
#         except Exception as e:
#             print("rabbit init error, please check the config", e)

#     @classmethod
#     def bind_queue_exchange(cls, queue, exchange, routing_key):
#         """
#         1、首先，如果queue和exchange不存在先创建；
#         2、绑定queue和exchange
#         """
#         channel = cls.connection.channel()
#         # 声明queue，如不存在，则创建
#         # channel.queue_declare(queue=queue, durable=True, arguments={'x-message-ttl': 259200000})
#         # 声明exchange，如不存在，则创建
#         channel.exchange_declare(exchange=exchange, durable=True, exchange_type='fanout')
#         # 绑定queue和exchange
#         # channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
#         cls.connection.close()