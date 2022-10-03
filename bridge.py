from curses import tparm
from selectors import EpollSelector
import threading
import rospy
import sys
from threading import Thread, Timer
import paho.mqtt.client as mqtt
from importlib import import_module
from std_msgs.msg import String, Int32, Int32MultiArray, Float32MultiArray, Float64MultiArray

def _finished_from_ros():
    print('{Ros->Mqtt} Transfer Finished : Received message from ROS and waiting for new message ...')

def _finished_from_mqtt():
    print('{Mqtt->Ros} Transfer Finished : Received message from MQTT and waiting for new message ...')

def _start_mqtt():
    print('{Mqtt->Ros} Waiting for new message ...')

def _start_ros():
    print('{Ros->Mqtt} Waiting for new message ...')

class RosToMqttBridge(Thread):
    def __init__(self):
        Thread.__init__(self)

        # Build the connection to MQTT broker
        self.host       = 'localhost'
        self.port       = 1883
        self.qos        = 0
        self.client                 = mqtt.Client('Ros-to-Mqtt')
        self.client.connect(self.host, self.port)
        self._ros_timer = Timer(2.0, _start_ros)
        self._ros_timer.start()

        # List the topic names and type of these message
        tp_list = rospy.get_published_topics()
        print(f'ROS topic :')
        for topic, msg_name in tp_list:
            msg_pkg, msg_type_name = msg_name.split('/')
            if msg_type_name != 'Log' and msg_type_name != 'Clock':
                print(f'            {topic} : message {msg_type_name}')
                msg_type = getattr(import_module(msg_pkg + '.msg'), msg_type_name)
                rospy.Subscriber(topic, msg_type, self._ros_callback, topic)

    def _ros_callback(self, message, topic):
        # Change the message type of ROS, recommened convert to string type
        if type(message.data) == tuple:
            ros_message = str(message.data)
        else:
            ros_message = message.data
        self.client.publish(topic, ros_message, self.qos)
        self._ros_timer.cancel()
        self._ros_timer = Timer(2.0, _finished_from_ros)
        self._ros_timer.start()

    def run(self):
        self.client.loop_start()
        rospy.spin()

class MqttToRosBridge(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host       = 'localhost'
        self.port       = 1883
        self.client                 = mqtt.Client('Mqtt-to-Ros')
        self.client.connect(self.host, self.port)
        self._mqtt_timer            = Timer(600.0, _start_mqtt)
        self._mqtt_timer.start()
    
    def on_message(self, client, userdata, msg):
        # Stop timer when received the message
        self._mqtt_timer.cancel()
        mqtt_message = msg.payload.decode()

        # Publish the mqtt message to ROS
        rospy.Publisher(msg.topic, String, queue_size=100).publish(mqtt_message)
        # # Start timer again
        self._mqtt_timer            = Timer(2.0, _finished_from_mqtt)
        self._mqtt_timer.start()
    
    def run(self):
        self.client.on_message      = self.on_message
        self.client.loop_start()
        self.client.subscribe('/exvis/sub/#')
        print(f'MQTT topic:')
        print(f'            /exvis/sub/#')

def main():
    try:
        print('\n--------------------------------- Start the ROS-MQTT bridge ---------------------------------\n\n')
        print('Note : Press [Ctrl+c] to stop the process.')
        rospy.init_node('bridge_node', anonymous=True)
        t1 = RosToMqttBridge()
        t2 = MqttToRosBridge()
        # Threading for reminding the stage of received message
        t1.start()
        t2.start()
    except KeyboardInterrupt:
        print('Stop to run the ROS-MQTT bridge ...')
        mqtt.Client.disconnect()
        sys.exit()

if __name__ == '__main__':
    main()