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
| `ros_server`      | ROS server |
| `mqtt_broker`     | MQTT broker (mosquitto) |
| `tester`          | 1st pane (0): MQTT subscriber (subscribe from ROS publisher), 2nd pane (1): ROS subscriber (subscribe from MQTT publisher), 3rd pane (2): ROS publisher, and 4st pane (3): MQTT publisher |

```
tester's window
.-----------------------.-----------------------.
| (0)                   | (1)                   |
|                       |                       |
|                       |                       |
|                       |                       |
|-----------------------|-----------------------|
| (2)                   | (3)                   |
|                       |                       |
|                       |                       |
|                       |                       |
|-------------.---------'----.------------------|
|0:ros_server |1:mqtt_broker |2:tester          |
'-------------'--------------'------------------'
```

2. Open the new terminal and launch the `bridge.py` script.

```script
$ python3 bridge.py
```