from random import randint as rnd
import paho.mqtt.client as mqtt
import time

client = mqtt.Client("Publisher")  # создание клиента

client.connect("127.0.0.1", 1883, 60)  # подключение к брокеру
client.loop_start()  # start the loop


while True:
    rand_list = [rnd(0, 1) for i in range(3)]             # данные для цвета
    rand_speed = rnd(5, 30)                               # данные для скорости
    client.publish("block", str(rand_list[0])+', '+str(rand_list[1])+', ' +
                   str(rand_list[2]))
    client.publish("speed", rand_speed)
    time.sleep(1)
