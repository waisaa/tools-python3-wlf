

def todo():
    """"""
    pass


# 作者：待到花开
# 链接：https://www.zhihu.com/question/485067313/answer/3431521612
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

# from paho.mqtt import client as mqtt
# import json
# import random
# from threading import Thread

# class MqttRoad():
#     def __init__(self, mqtt_host, mqtt_port, mqtt_keepalive, client_id, protocol=mqtt.MQTTv31):
#         self.myClient = mqtt.Client(client_id, protocol=protocol)
#         self.myClient.on_connect = self.on_connect
#         self.myClient.on_message = self.on_message
#         self.myClient.on_publish = self.on_publish
#         # self.myClient.connect_async(mqtt_host, mqtt_port, mqtt_keepalive) # 异步数据发送
#         self.myClient.connect(mqtt_host, mqtt_port, mqtt_keepalive)  # 同步数据发送
#         # self.myClient.loop_forever()  # 保持连接

#     def on_connect(self, client, userdata, flags, rc):
#         """
#        连接回调 连接主题(成功,失败)都会调用此函数
#        :param client: 此回调的客户机实例
#        :param userData:在Client（）或userdata_set（）设置的私有用户用户数据
#        :param flags:代理发送的响应标志
#        :param rc:连接结果, 0:连接成功 1:连接被拒绝-协议版本不正确 2:连接被拒绝-客户端标识符无效 3:连接被拒绝-服务器不可用
#        4:连接被拒绝-用户名或密码错误 5:连接被拒绝-未授权 6-255:当前未使用。
#        :param reasonCode:mqttv5.0原因码：reasonCode类的实例
#        :param properties:从代理返回的mqttv5.0属性,对于MQTT v3.1和v3.1.1，未提供属性，但用于兼容性 对于mqttv5.0，官方建议添加properties=None。
#        :return:
#        """
#         print("Connected with result code: " + str(rc))

#     def on_message(self, client, userdata, msg):
#         """
#        消息回调
#        message: MQTTMessage的实例。这是一个包含成员主题、负载、qos和保留的类
#        :return:
#        """
#         print("接收来自主体:" + msg.topic + " 的消息内容:" + str(msg.payload.decode('utf-8')))

#     def on_subscribe(self, client, userdata, mid, granted_qos):
#         """
#        订阅回调
#        :param mid:匹配从相应的subscribe（）调用
#        :param grated_qos:给出代理的qos级别的整数列表,为每个不同的订阅请求授予。
#        :return:
#        """
#         print("On Subscribed: qos = %d" % granted_qos)
#         pass

#     def on_unsubscribe(self, client, userdata, mid):
#         """
#        取消订阅
#        :param mid:匹配从相应的unsubscribe（）调用。
#        :return:
#        """
#         print("On unSubscribed: qos = %d" % mid)
#         pass

#     def on_publish(self, client, userdata, mid):
#         """
#         消息发布回调
#         对于QoS级别为1和2的消息，这意味着握手已完成。对于QoS 0，这意味着消息已经离开了客户。
#         这个回调很重要，因为即使publish（）调用返回成功，并不总是意味着消息已发送
#         :param mid:匹配从相应的publish（）调用，以允许跟踪传出消息。
#         :return:
#         """
#         print("On onPublish: qos = %d" % mid)
#         pass

#     def on_disconnect(self, client, userdata, rc):
#         """
#         断开连接
#         :param rc:断开连接的结果
#         :return:
#         """
#         print("Unexpected disconnection rc = " + str(rc))
#         pass

#     def publishMes(self, topic, qos=2):
#         """
#         向指定主体发布消息内容
#         :param topic: 主体名称
#         :param msg: 消息内容
#         :param qos: 发送方式
#         :return:
#         """
#         while True:
#             msg = input("请输入发送信息：")
#             self.myClient.publish(topic, msg, qos=qos)

#     def subscribeMes(self, topic):
#         """
#         接收指定主体发布的消息
#         :param topic:主体名称
#         :return:
#         """
#         self.myClient.subscribe(topic)
#         self.myClient.loop_forever()

# if __name__ == '__main__':
#     topic = "/test/mqtt"
#     pub_client_id = f'python-mqtt-{random.randint(0, 1000)}' # 发布客户端ID
#     sub_client_id = f'python-mqtt-{random.randint(0, 1000)}' # 订阅客户端ID
#     pub_myclien = MqttRoad("127.0.0.1", 1883, 600, pub_client_id) # 生成发布客户端ID
#     sub_myclien = MqttRoad("127.0.0.1", 1883, 600, sub_client_id) # 生成接收客户端ID  （客户端id不能重复）
#     pub_thread = Thread(target=pub_myclien.publishMes, name='pub', kwargs={'topic': topic})  # 创建线程进行消息发布
#     sub_thread = Thread(target=sub_myclien.subscribeMes, name='sub', kwargs={'topic': topic}) # 创建线程进行消息接收
#     sub_thread.start() # 启动消息接收的线程
#     pub_thread.start() # 启动消息发布的线程
#     pub_thread.join() # 等待线程结束进行回收
#     sub_thread.join() # 等待线程结束进行回收