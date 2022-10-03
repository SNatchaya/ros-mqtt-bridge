from curses import tparm
from selectors import EpollSelector
import threading
import rospy
import sys
import threading
import paho.mqtt.client as mqtt
from importlib import import_module
from std_msgs.msg import String, Int32, Int32MultiArray, Float32MultiArray 

def _finished_from_ros():
    print('{Ros->Mqtt} Transfer Finished : Received message from ROS and waiting for new message ...')

def _finished_from_mqtt():
    print('{Mqtt->Ros} Transfer Finished : Received message from MQTT and waiting for new message ...')

def _start_mqtt():
    print('{Mqtt->Ros} Waiting for new message ...')

def _start_ros():
    print('{Ros->Mqtt} Waiting for new message ...')

class RosToMqttBridge(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # Build the connection to MQTT broker
        self.host       = 'localhost'
        self.port       = 1883
        self.qos        = 0
        self.client                 = mqtt.Client('Ros-to-Mqtt')
        self.client.connect(self.host, self.port)

        # List the topic names and type of these message
        tp_list = rospy.get_published_topics()
        print(tp_list)
        print(f'ROS topic :')
        for topic, msg_name in tp_list:
            msg_pkg, msg_type_name = msg_name.split('/')
            if msg_type_name != 'Log':
                print(f'            {topic} : message {msg_type_name}')
                msg_type = getattr(import_module(msg_pkg + '.msg'), msg_type_name)
                rospy.Subscriber(topic, msg_type, self._ros_callback, topic)

    def _ros_callback(self, message, topic):
        self._ros_timer.cancel()
        self._ros_timer = threading.Timer(2.0, _finished_from_ros)
        # Change the message type of ROS, recommened convert to string type
        if type(message.data) == tuple:
            ros_message = str(message.data)
        else:
            ros_message = message.data
        
        self.client.publish(topic, ros_message, self.qos)
        self._ros_timer.start()

    def run(self):
        self.client.loop_start()
        self._ros_timer = threading.Timer(1.0, _start_ros)
        self._ros_timer.start()
        rospy.spin()
        # try:
        #     rospy.spin()
        # except KeyboardInterrupt:
        #     self.client.loop_stop()
        #     self.client.disconnect()
        #     # with open(str(datetime.now) + '.json', 'w') as json_file:
        #     #     json.dump(mqtt_client.exo_data, json_file)
        #     sys.exit(1)

class MqttToRosBridge(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.host       = 'localhost'
        self.port       = 1883
        self.client                 = mqtt.Client('Mqtt-to-Ros')
        self.client.connect(self.host, self.port)
    
    def on_message(self, client, userdata, msg):
        # Stop timer when received the message
        self._mqtt_timer.cancel()
        mqtt_message = msg.payload.decode()

        # Publish the mqtt message to ROS
        rospy.Publisher(msg.topic, String, queue_size=100).publish(mqtt_message)
        # # Start timer again
        self._mqtt_timer            = threading.Timer(2.0, _finished_from_mqtt)
        self._mqtt_timer.start()
    
    def run(self):
        self._mqtt_timer            = threading.Timer(600.0, _start_mqtt)
        self._mqtt_timer.start()
        self.client.on_message      = self.on_message
        self.client.loop_start()
        self.client.subscribe('/exvis/#')
        print(f'MQTT topic:')
        print(f'            /exvis/#')
        # try:
        #     self.client.loop_forever()
        # except KeyboardInterrupt:
        #     print('xxx')
        #     self.client.disconnect()
        #     sys.exit(1)
        # timer = threading.Timer(2.0, _finished_from_mqtt)
        # timer.start()

def main():
    try:
        print('\n------------------ Start the ROS-MQTT bridge ------------------\n')
        print('Press [Ctrl+c] to stop the process ...')
        rospy.init_node('bridge_node', anonymous=True)
        t1 = RosToMqttBridge()
        t2 = MqttToRosBridge()
        # Threading for reminding the stage of received message
        t1.start()
        t2.start()
    except KeyboardInterrupt:
        print('Stop to run the ROS-MQTT bridge ...')
        mqtt.Client.disconnect()
        sys.exit(1)

if __name__ == '__main__':
    main()