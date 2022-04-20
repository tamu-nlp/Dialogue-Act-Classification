import paho.mqtt.client as mqtt
from heartbeat_message import HeartbeatMessage

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

# 

class Coordinator():
  heartbeat = HeartbeatMessage
  def do_something_useful(self, client):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    print("do_something_useful")


class Mqtt:

  # TODO pass these in
  host = "localhost"
  port = 1883
  keepalive = 60
  bind_address = ""

  def on_connect(client, userdata, flags, rc):

    # Paho return code definitions
    if(rc == 0):
      print("Connection successful")
      userdata.do_something_useful(client)
    elif(rc == 1):
      print("Connection refused - incorrect protocol version")
    elif(rc == 2):
      print("Connection refused - invalid client identifier")
    elif(rc == 3):
      print("Connection refused - server unavailable")
    elif(rc == 4):
      print("Connection refused - bad username or password")
    elif(rc == 5):
      print("Connection refused - not authorised")
    else:
      print("Connection refused - return code " + str(rc))


  # The callback for when a PUBLISH message is received from the server.
  def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

  client = mqtt.Client(userdata=Coordinator())
  client.on_connect = on_connect
  client.on_message = on_message

  print("TDAC connecting to Message Bus... ")
  client.connect(host, port, keepalive, bind_address)
  client.loop_start()

  # Blocking call that processes network traffic, dispatches callbacks and
  # handles reconnecting.
  # Other loop*() functions are available that give a threaded interface and a
  # manual interface.
