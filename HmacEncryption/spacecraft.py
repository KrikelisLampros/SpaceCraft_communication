from space_comm import transmitter
import time

class spacecraft:

    def __init__(self,id):
        self.id = id
        self.pos_x = 10
        self.pos_y = 10
        msg_type = 0 # position broadcast
        b = bytes([msg_type,self.id,self.pos_x,self.pos_y])
        self.t = transmitter(str(self.id))
        self.t.transmit(b)
        

    def move_spacecraft(self,direction,distance):

        if direction == 1:
            self.pos_x = self.pos_x + distance
        if direction == 2:
            self.pos_y = self.pos_y + distance
        if direction == 3:
            self.pos_x = self.pos_x - distance
        if direction == 4:
            self.pos_y = self.pos_y - distance
        self.log("New position : {} {}".format(self.pos_x,self.pos_y))
        time.sleep(1)
        msg_type = 0 # position broadcast
        b = bytes([msg_type,self.id,self.pos_x,self.pos_y])
        self.t = transmitter(str(self.id))
        self.t.transmit(b)


    def process_msg(self,b):
        self.log("------------------")
        self.log("received a message")
        if int(b[0]) == 1: # if msg is of type command
            self.log("received a command message")
            id = int(b[1])
            if id == self.id:
                self.log("message for me")
                direction = int(b[2])
                distance = int(b[3])
                if direction < 1 or direction > 4 or distance < 0 or distance >10:
                    self.log("Message rejected")
                else:
                    self.move_spacecraft(direction,distance)
            else:
                self.log("message not for me")
        else:
            self.log("not a command message")

    def get_position(self):
        return self.pos_x,self.pos_y

    def log(self,msg):
        print("logging... "+str(self.id)+" "+msg)

