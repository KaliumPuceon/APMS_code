#! /usr/bin/python3

import camera
import rfid
import scale
import web

import time
import os
import sys

def main():

    print("Initialize Camera")
    cam_loop = camera.capture(0)
    cam_loop.setDaemon(True)
    cam_loop.start()
    print("Camera started")

#    print("Starting scale")
#    scale_loop = scale.scale()
#    scale_loop.setDaemon(true)
#    scale_loop.start()
#    print("Scale ready")

    print("Start RFID scanner")
    rfid_loop = rfid.rfid()
    rfid_loop.setDaemon(True)
    rfid_loop.start()
    print("Scanner started")

    try:

        while True:
            time.sleep(0.05)
            if rfid_loop.tag_arrived: # if new tag, fire camera and reset flag
                print("Tag Arrived")
                cam_loop.request_buffer()
                rfid_loop.tag_arrived = False

            #if scale_loop.scale_arrived: # if new tag, fire camera and reset flag
            #    cam_loop.request_buffer()
            #    scale_loop.scale_arrived = False


    except KeyboardInterrupt:
        cam_loop.running = False
        rfid.running = False

        sys.exit();

if __name__ == "__main__":
    main()
