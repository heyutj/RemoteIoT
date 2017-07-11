import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
mqttc.connect("127.0.0.1", port=1883, keepalive=60, bind_address="")
mqttc.loop_start()
# {"type":"ctrl","dev_type":"video","action":"on"}
while True:
    data=input()
    mqttc.publish('/IoT/ctrl',bytes(data,"utf-8"))