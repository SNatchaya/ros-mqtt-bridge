# ROS-MQTT bridge

The ROS-MQTT bridge provides a feature that allows for bidirectional communication between ROS and MQTT.

## Demo

> Note: launch the `test_script.py` before launch the `bridge.py`, due to ROS-MQTT bridge can get the topic and message type from ros automatically.

1.  Open the terminal,and xxx. (Note)

```script
$ chmod +x test_bridge.sh
```

2. Launch the `test_bridge.sh` script to use the ROS server, mqtt broker, publisher, and subscriber.

```script
$ ./test_bridge.sh
```

Each window in tmux terminal means ...

| Window | Description |
| ------ | ----------- |
| `roscore_server`  | ROS server |
| `mqtt_broker`     | MQTT broker (mosquitto) |
| `client`          | ROS and MQTT sucscriber |
| `publisher`       | ROS and MQTT publisher |

3. Open the new terminal and run the `bridge.py` script.

```script
$ python3 bridge.py
```