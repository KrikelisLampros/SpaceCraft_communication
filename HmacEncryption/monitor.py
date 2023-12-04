import time

import paho.mqtt.client as mqtt #import the client1

spaceships_positions={}

broker_address="127.0.0.1"

def draw_space():
    global spaceships_positions
    for i in reversed(list(range(0,20))):
        row=""
        for j in range(0,20):
            s =" - "
            for k in spaceships_positions.keys():
                pos_x = spaceships_positions[k][0]
                pos_y = spaceships_positions[k][1]
                if pos_x == i and pos_y == j:
                    s = " "+str(k)+" "
            if i == 10 and j == 10:
                 s =" b "
            row=row+s
        print(row)
    print(spaceships_positions)


def on_message(client,userdata, message):
    global spaceships_positions
    msg = message.payload
    if int(msg[0]) == 0:
        id = int(msg[1])
        pos_x = int(msg[2])
        pos_y = int(msg[3])
    
        print("Spacecraft with id : {} is at ({},{})".format(id,pos_x,pos_y))
        spaceships_positions[id] = (pos_x,pos_y)
        draw_space()


client = mqtt.Client("drawer") 
client.on_message = on_message 
client.connect(broker_address) 
client.loop_start()
client.subscribe("space")

while True:
    time.sleep(10)