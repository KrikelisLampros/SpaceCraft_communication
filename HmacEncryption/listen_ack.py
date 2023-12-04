from space_comm import receiver


class AcknowledgementHandler:
    def __init__(self):
        self.r = receiver("listen_ack ... ")

    def listen_ack_msg(self):
        while True:
            msg = self.r.listen_single_msg()
            # ack_msg_inv = bytes([msg_type, id, ack])

            self.msg_type = msg[0]
            self.id = msg[1]
            self.check_msg = msg[2]
            # Here we filter the acknowledgment command from the other 2
            if self.msg_type == 2:
                print(
                    f"This is an acknowledgment msg : {self.msg_type} {self.id} {self.check_msg}"
                )
                self.handle_ack_msg(self.check_msg)

            print("msg not for me ")

    def handle_ack_msg(self, check_msg):
        if self.check_msg == 0:
            print("The message has been corrupted ")
        elif self.check_msg == 1:
            print(f"The message for spacecraft {self.id} has been sent successfully.")


if __name__ == "__main__":
    ack_handler = AcknowledgementHandler()
    ack_handler.listen_ack_msg()
