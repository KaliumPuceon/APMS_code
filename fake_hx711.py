#! /usr/bin/python3

import time

class HX711:

    def __init__(self, dout, pd_sck, gain=128):

        self.filename='/tmp/scale_reading.txt'

    def get_weight(self,num):
        with open(self.filename) as file:
            data = file.read()
            time.sleep(0.01)
            return (float(data))

    def set_reading_format(self, text, text2):
        return

    def set_reference_unit(self,text):
        return

    def power_up(self):
        return

    def reset(self):
        return

    def tare(self):
        return
        


