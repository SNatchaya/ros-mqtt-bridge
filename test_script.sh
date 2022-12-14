#!/bin/bash

session='bridge_test'

# Create 'bridge_test' session, which used for simulating the ROS-MQTT bridge
tmux new-session -d -s $session

# Run the ROS server in the 1st window
window=0
tmux rename-window -t $session:$window 'ros_server'
tmux send-keys -t $session:$window 'roscore' ENTER

# Run the mqtt server in the 2nd window
window=1
tmux new-window -t $session:$window -n 'mqtt_broker'
tmux send-keys -t $session:$window 'mosquitto -v' ENTER

# Run the ros client and mqtt client in the 3rd window
window=2
tmux new-window -t $session:$window -n 'tester'
tmux split-window -h
tmux split-window -v
tmux select-pane -t 0
# using rostopic echo <topic> to display the received mqtt messages
!(sleep 1 && tmux send-keys -t $session:$window 'mosquitto_sub -h localhost -t /exvis/#' ENTER)  
tmux select-pane -t 1       
# using mosquitto_sub -h localhost -t <topics> to display the received ros messages
!(sleep 1 && tmux send-keys -t $session:$window 'rostopic echo /exvis/sub/test' ENTER)  
tmux select-pane -t 0 
tmux split-window -v  \; send-keys 'cd tester' ENTER \; send-keys 'rosbag play rosbag_test.bag' ENTER
tmux select-pane -t 3 \; send-keys 'cd tester' ENTER \; send-keys 'python3 mqtt_pub.py' ENTER

tmux attach-session -t $session