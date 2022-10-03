#!/bin/bash

att() {
    [ -n "${TMUX:-}" ] &&
        tmux switch-client -t '=test_bridge' ||
        tmux attach-session -t '=test_bridge'
}

if tmux has-session -t '=test_bridge' 2> /dev/null; then
    att
    exit 0
fi


tmux new-session -d -s test_bridge

tmux new-window -d -t '=test_bridge' -n btop 
tmux send-keys -t '=test_bridge:=btop' 'btop' ENTER

tmux new-window -d -t '=test_bridge' -n broker
tmux send-keys -t '=test_bridge:=broker' 'roscore' ENTER
tmux split-window -h -t '=test_bridge:=broker' 
tmux send-keys -t '=test_bridge:=broker' 'mosquitto -v' ENTER

# tmux new-window -d -t '=test_bridge' -n tester -c /home/bb/Desktop/bagfiles/S5/DZ
# tmux send-keys -t '=test_bridge:tester' 'rosbag play 2022-08-27-14-58-07.bag' ENTER
# tmux split-keys -h -t '=test_bridge:=tester'
# tmux send-keys -t '=test_bridge:tester' 'cd /home/bb/catkin_ws/src/exobic_project/scripts python3 bridge.py'
# tmux split-keys -h -t '=test_bridge:=tester':0 -c /home/bb/Desktop/mqtt_test
# tmux send-keys -t '=test_bridge:=tester' 'python3 pub.py'

att
