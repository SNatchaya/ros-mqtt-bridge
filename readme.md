# ROS-MQTT bridge

The ROS-MQTT bridge provides a feature that allows for bidirectional communication between ROS and MQTT.

## Demo

> Note: launch the `test_script.py` before launch the `bridge.py`, due to ROS-MQTT bridge can get the topic and message type from ros automatically.

1. Launch the `test_bridge.sh` bash script to use the ROS server, mqtt broker, publisher, and subscriber.

```script
$ bash test_bridge.sh
```

Each window in tmux terminal means ...

| Window | Description |
| ------ | ----------- |
| `roscore_server`  | ROS server |
| `mqtt_broker`     | MQTT broker (mosquitto) |
| `tester`          | 1st pane: MQTT subscriber (subscribe from ROS publisher), 2nd pane: ROS subscriber (subscribe from MQTT publisher), 3rd pane: ROS publisher, and 4st pane: MQTT publisher |

2. Open the new terminal and launch the `bridge.py` script.

```script
$ python3 bridge.py
```