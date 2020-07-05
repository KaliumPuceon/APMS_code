import sys
import os
import time
import collections
import cv2
import threading
import tuxconf as tc

class capture(threading.Thread):

    def __init__(self, cam_id):
        threading.Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.save_request = False
        self.lock_request = False
        self.cam_id = cam_id
        self.cam = cv2.VideoCapture(cam_id)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,tc.image_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,tc.image_height)
        self.cam.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        self.cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self.count = 0
        self.frames_remaining = 0
        self.image_ring = collections.deque("",tc.pre_buffer+tc.post_buffer)
        self.main_image = self.take_pic()
        self.filename = ""

        try:    # Create storage dirs
            os.makedirs(tc.image_dir)
        except FileExistsError:
            print("Image dir already exists")


    def run(self):

        print("Camera "+str(self.cam_id) + " is running")
        while self.running:

            if not (self.lock_request): # take pictures if not busy saving
                self.image_ring.append(self.take_pic())

            time.sleep(tc.frame_period)

            if self.save_request: # if a save is requested, countdown
                self.frames_remaining -= 1

                if self.frames_remaining <= 0:

                    self.save_request = False
                    self.save_buffer()

    
    def request_buffer(self): # Make a request to save buffer

        if not(self.save_request or self.lock_request):
            print("Save requested")

            self.main_image = self.take_pic() # Choose the core image

            self.frames_remaining = tc.post_buffer
            self.save_request = True
            self.filename = tc.image_dir+str(int(time.time())) # Set dir name

        else:
            print("Save already requested")


    def save_buffer(self): # Save contents of buffer now
        
        if not(self.lock_request):

            print("Start saving buffer")
            self.lock_request = True

            localbuffer = list(self.image_ring) # make value copy of array

            os.makedirs(self.filename)


            cv2.imwrite(self.filename+"/main.jpg", self.main_image) # store core image
            fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
            videowriter = cv2.VideoWriter(self.filename+"/capture.mp4",fourcc, 1/tc.frame_period, (tc.image_width,tc.image_height))

            for image in self.image_ring:

                videowriter.write(image) # create video file


            videowriter.release()
            print("buffer saved")

            self.lock_request = False

        else:
            print("Buffer already being saved")


    def take_pic(self):

        conf, img = self.cam.read()

        if conf:
            return(img)
            
def main():

    try:
        os.makedirs(tc.image_dir)
    except FileExistsError:
        print("Image dir already exists")

    cam_loop = capture(0)
    cam_loop.setDaemon(True)
    cam_loop.start()

    ans = ""

    while ans != 'q':

        ans = input("Enter Command > ")
        if ans == "show":
            print(str(len(cam_loop.image_ring)) + " items in ring 0")

        elif ans == "cap":
            print("capture requested")
            cam_loop.request_buffer()

        else:
            print("iunno man")


    cam_loop.running = False

    sys.exit()

if __name__ == "__main__":
    main()
