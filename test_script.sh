#!/bin/bash

session='bridge_test'

# Create 'bridge_test' session, which used for simulating the ROS-MQTT bridge
tmux new-session -d -s $session

# Run the ROS server in the 1st window
window=0
tmux rename-window -t $session:$window 'roscore_server'
tmux send-keys -t $session:$window 'roscore' ENTER

# Run the mqtt server in the 2nd window
window=1
tmux new-window -t $session:$window -n 'mqtt_broker'
tmux send-keys -t $session:$window 'mosquitto -v' ENTER

# Run the ros client and mqtt client in the 3rd window
window=2
tmux new-window -t $session:$window -n 'scriber'
# using rostopic echo <topic> to display the received mqtt messages
!(sleep 1 && tmux send-keys -t $session:$window 'rostopic echo /exvis/sub/test' ENTER)              
tmux split-window -h
# using mosquitto_sub -h localhost -t <topics> to display the received ros messages
!(sleep 1 && tmux send-keys -t $session:$window 'mosquitto_sub -h localhost -t /exvis/#' ENTER )    

# Run the publisher in the 4st window. The publisher files locate in scripts folder.
window=3
tmux new-window -t $session:$window -n 'publisher'
tmux send-keys -t $session:$window 'cd scripts' ENTER
# Mimick the ros publisher using rosbag from .bag file
tmux send-keys -t $session:$window 'rosbag play rosbag_test.bag'
tmux split-window -h
tmux send-keys -t $session:$window 'cd scripts' ENTER
# Mimick the mqtt publisher using mqtt_pub.py
tmux send-keys -t $session:$window 'python3 mqtt_pub.py'

tmux attach-session -t $session