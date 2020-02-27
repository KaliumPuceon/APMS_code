import serial
import time
import threading
import tuxconf as tc

class rfid(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.running = True
        self.device = serial.Serial(tc.serial_path,tc.serial_baud,timeout=5)
        self.tag_arrived = False


    def run(self):
    
        while self.running:
            
            line = self.device.readline().decode('ascii')
            tag_time = str(int(time.time()))

            if (len(line) > 2):
                print("[TAG] "+line)
                self.tag_arrived = True
                
                with open(tc.serial_log, 'a') as file:
                    file.write(tag_time+","+line+"\n")

        self.device.close()


