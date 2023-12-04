from math import dist
import time, sys
from datetime import datetime
from threading import Thread, Lock
from space_comm import receiver, transmitter
from spacecraft import spacecraft

import hmac, hashlib


class spacecraft_inst:
    def __init__(self, id, lock):
        task = open("task", "r").readline().rstrip("\n")
        if task == "1.3" or task == "1.4":
            comm_failure = True
        else:
            comm_failure = False

        self.s = spacecraft(id)

        self.r = receiver("spacecraft_" + str(id), comm_failure)
        self.lock = lock

    def launch(self):
        while True:
            time.sleep(0.01)
            msg = self.r.listen_single_msg()
            msg = self.handle_msg(msg)
            self.lock.acquire()
            self.s.process_msg(msg)
            self.lock.release()

    # Handle incoming messages
    def handle_msg(self, msg):
        while True:
            # If the incoming msg is less than 4 bytes it must be a report msg so we dont do anything
            # we only care about the command msg ( base_station masseges )

            if len(msg) <= 4:
                return msg

            # Here basicly we filter the incoming msg
            # From the Base station which contains the sig and the msg

            sig = msg[-4:]
            var1 = list(msg[:-4])
            new_msg = msg[:-4]
            msg_type = var1[0]
            msg_id = var1[1]
            msg_dir = var1[2]
            msg_dist = var1[3]

            msg_ack_type = 2  # is the acknowledgment command

            # Here we check if the incoming command from base station is in the correct spacecraft
            if msg_id != self.s.id:
                # We return the 200 200 200 200 value because we want something that does not make any sense
                # we can not type negative numbers. in bytes functions only allows the range  0-256
                return bytes([200, 200, 200, 200])

            output = self.handle_corruption(sig, new_msg)

            # This if statment check if the output/sig is valid or not
            if str(output) != "valid":
                print("Invalid ", self.s.id)
                ack_inv = 0
                self.prepare_ack_msg(msg_ack_type, self.s.id, ack_inv)

                return bytes([200, 200, 200, 200])

            # print("this is a valid msg ", self.s.id)
            # Task 1.2
            f = open(str(self.s.id) + ".log", "a+")
            timestamp = datetime.now()
            f.write(str(timestamp))
            f.write(str(msg_dir))
            f.write(str(msg_dist))
            f.close()

            ack_v = 1
            self.prepare_ack_msg(msg_ack_type, self.s.id, ack_v)

            return msg

    # Hashing the message for Task 1.3
    # The perpuse of this Func is to check  the msg for coraption with the help of the hash function
    def handle_corruption(self, tag, new_msg):
        basestation_key = "secret2"

        mac = hmac.new(bytes(basestation_key, "utf-8"), new_msg, hashlib.sha256)
        # digest returns the hash function as bytes
        temp = mac.digest()
        sig = temp[-4:]

        if tag == sig:
            output = "valid"
            return output
        else:
            output = "invalid"
            return output

    # Task 1.4
    # handling  The format of the transmetted Acknowledgement msg
    def prepare_ack_msg(self, msg_type, id, ack):
        self.t = transmitter("From Spacecraft to Base")
        ack_msg = bytes([msg_type, id, ack])
        self.t.transmit(ack_msg)
