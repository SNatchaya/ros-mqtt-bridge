#!/bin/bash

tmux new-session -d -s client \; split-window -h ;\
tmux send-keys -t client.0 'rostopic echo /exvis/test' ENTER
tmux send-keys -t client.1 'mosquitto_sub -h localhost -t /exvis/timeStampCAN' ENTER
tmux a -t client
