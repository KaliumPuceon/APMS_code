import serial
import time
import threading
import tuxconf as tc
import sys

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


def main():
    print("Start RFID scanner")
    rfid_loop = rfid()
    rfid_loop.setDaemon(True)
    rfid_loop.start()
    print("Scanner started")

    try:
        while True:
            continue
    except KeyboardInterrupt:
        rfid.running=False
        sys.exit()


if __name__ == "__main__":
    main()
