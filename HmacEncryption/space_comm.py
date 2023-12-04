import paho.mqtt.client as mqtt #import the client1
import time,random,sys,math
import random

def on_message(client, userdata, message):  
    print("received: "+message.payload.hex())   
    
def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])   

class transmitter:
    def __init__(self,_client_name):
        self.broker_address="127.0.0.1"
        self.topic = "space"
        self.client = mqtt.Client(_client_name)
        self.client.connect(self.broker_address)


    def transmit(self,message):
        self.client.publish(self.topic,message)  

class receiver:
    def __init__(self,_client_name, com_failure = False):  
        self.broker_address="127.0.0.1"  
        self.topic = "space"
        self.client = mqtt.Client(_client_name)  
        self.client.on_message=self.on_message 
        self.client.connect(self.broker_address) 
        self.client.loop_start()
        self.client.subscribe(self.topic)
        self.waiting = True
        self.msg = None
        self.com_failure = com_failure

    def on_message(self,client,userdata, message):
        #print("received data: "+message.payload.hex())
        self.msg = message.payload
        self.waiting = False

    def listen(self):
        while True:
            time.sleep(10)

    def listen_single_msg(self):
        self.waiting = True
        while self.waiting:
            time.sleep(0.1)
        if self.msg[0] == 1:
            dir = self.msg[2]
            dist = self.msg[3]
            msg = list(self.msg)
            if self.com_failure:
                dir = self.randomize_bytes(dir)
                dist = self.randomize_bytes(dist)
                msg[2] = dir
                msg[3] = dist
        else:
            msg = list(self.msg)
        return(bytes(msg))

    def randomize_bytes(self,b):
        if random.randint(0,10)>5:
            rand_effect = bytes([random.randint(1,4)])
            bf = byte_xor(bytes(b),rand_effect)
            return int.from_bytes(bf,"big")
        else:
            return b