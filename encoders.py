import RPi.GPIO as GPIO
from time import sleep
from threading import Thread
from time import sleep


num_encoders = 4


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
pins_encoder = [21,20,16, 13,19,26, 22,17,27, 25,24,23] # btn, dt, clk


class Encoders():
    flag =  True
    def __init__(self) -> None:
        self.flag = True
        self.values = [[False for n in range(4)] for i in range(num_encoders)]
        self.last_values =[[False for n in range(4)] for i in range(num_encoders)]
        self.msg = [[None, None] for i in range(4)]
        self.pins = pins_encoder
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN)
        


    def start(self):
        Thread(target=self.read).start()

    def read(self):
        while Encoders.flag:
            values = []
            for pin in self.pins:
                value = True if GPIO.input(pin) == 0 else False
                values.append(value)  
            # print(values)
            sleep(0.01)
            self.map_values(values)
            sleep(0.01)


    def map_values(self,values):
        self.values = []
        for i in range(num_encoders):
            self.values.append(values[3*i:3*i+3])
            # print(self.values)
        self.msg =  self.evaluate_encoders()

    def get_msg(self):
        _msg = self.msg
        self.msg = [[None, None] for i in range(3)]
        return _msg


    def evaluate_encoders(self):
        msg = []
        # print(self.values, self.last_values)
        for values, last_values in zip(self.values, self.last_values):
            #print(values)
            sub_msg = []
            # CLICK
            if values[0]  and last_values[0]:
                sub_msg.append(False)
            elif not values[0]  and last_values[0]:
                sub_msg.append(None)
            elif not values[0]  and not last_values[0]:
                sub_msg.append(None)
            elif values[0]  and not last_values[0]:
                sub_msg.append(True)

            # ENCODER
            if last_values[1] and last_values[2]:
                if values[1] and not values[2]:
                    sub_msg.append(1)
                elif not values[1] and values[2]:
                    sub_msg.append(-1)
                else:
                    sub_msg.append(None)
            else:
                sub_msg.append(None)
            msg.append(sub_msg)
        # if msg[0][0] == False or msg[0][1]:
            # print(msg)

        self.last_values = self.values
        # print(msg)
        return msg


if __name__ == '__main__':
    encoders = Encoders()
    encoders.start()
    try:
        while encoders.flag:
            # sleep(0.05)
            msg = encoders.get_msg()
            for i, n in zip(msg,range(len(msg))):
                if i[0] != None or i[1] != None:
                    print(msg, n)
    except KeyboardInterrupt:
        Encoders.flag = False