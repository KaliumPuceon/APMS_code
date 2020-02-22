import camera
import rfid
import scale
import web

import time
import os
import sys

def main():

    cam_loop = camera.capture(0)
    cam_loop.setDaemon(True)
    cam_loop.start()

    scale_loop = scale.scale()
    scale_loop.setDaemon(true)
    scale_loop.start()

    rfid_loop = rfid.rfid()
    rfid_loop.setDaemon(True)
    rfid_loop.start()

    try:

        while True:
            time.sleep(0.05)
            if rfid_loop.tag_arrived: # if new tag, fire camera and reset flag
                cam_loop.request_buffer()
                rfid_loop.tag_arrived = False

            if scale_loop.scale_arrived: # if new tag, fire camera and reset flag
                cam_loop.request_buffer()
                scale_loop.scale_arrived = False


        except KeyboardInterrupt:
            cam_loop.running = False
            rfid.running = False

            sys.exit();
