import paho.mqtt.client as mqtt

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

# 
class Mqtt():
  print("Python Message Bus Client")

  
  # The callback for when a CONNACK response is received from the server.
  def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("foo")

    print("subscribed to topic: foo")

  # The callback for when a PUBLISH message is received from the server.
  def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  client.connect("localhost", 1883, 60)  # TODO pass this in

  # Blocking call that processes network traffic, dispatches callbacks and
  # handles reconnecting.
  # Other loop*() functions are available that give a threaded interface and a
  # manual interface.
  client.loop_forever()
