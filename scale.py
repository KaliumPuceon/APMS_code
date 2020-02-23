import time
import collections
import threading
import tuxconf as tc

class scale(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.scale_arrived = False
        self.weigh_bins = []

        self.min_weight = 1.5
        self.max_weight = 5
        self.on_scale = False
        self.off_scale_count = 0

        self.increment = (5-1.5)/300

        self.reset_bins()
            

    def run(self):

        while self.running:

            value = self.read_scale()

            if (value > threshold) and (not self.on_scale):

                self.on_scale = True
                self.off_scale_count = 0

            if self.on_scale:
                valid_measure = self.assign_bin(value)

                if not valid_measure:
                    
                    self.off_scale_count += 1

                    if self.off_scale_count > 50:

                        self.on_scale = False
                        weight = self.guess_weight()
                        print("[SCALE] "+str(weight)+"kg")

                        self.reset_bins()

                        self.scale_arrived = True

                        weight_time = str(int(time.time()))

                        with open(tc.weight_log, 'a') as file:
                            myfile.write(weight_time+","+str(weight))

                        
            
            
    def assign_bin(self,value):

        for k in self.weigh_bins:

            if (value > k[1][0]) and (value < k[1][1]):

                k[0]+=1

                return True

        else:
                return False



    def reset_bins(self):

        for k in range(300):
            self.weigh_bins[k] = [0,(self.min_weight + (k*self.increment), self.max_weight + ((k+1)*self.increment))]
 
            

    def guess_weight(self):

        valid = 0
        total = 0
        maxcount = 0
        for k in self.weigh_bins:
            
            if k[0] > maxcount:
                maxcount = k[0]
                total = (k[0]*(k[1][0]+k[1][1])/2)
                valid = 1

            elif k[0] == maxcount:
                total += (k[0]*(k[1][0]+k[1][1])/2)
                valid += 1

            else:
                pass

        return(total/valid)



    def read_scale(self):
        return 4;


