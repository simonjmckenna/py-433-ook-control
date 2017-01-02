#!/usr/bin/python

import ctypes, time

#--- Microsecond delay functions: ---

# Class for high resolution timer using libc and uSleep()
class hrSleep():

    #store error compensation
    compensation = 0

    # libc shared library:
    libc = ctypes.CDLL('libc.so.6')


    def __init(self):
        # initialise compensaiton
        compensation = 0

    def clearCompensation(self):
        self.compensation=0

    def SetCompensation(self,basedelay,turns):
        values= [0] * turns 
        for test in range (0,turns):
           values[test] = time.time()
           self.usDelay(basedelay)       

        total_error = 0
        for test in range (2,turns):
           period =  (values[test] - values[test-1])* 1e6
           total_error += period - basedelay
 
        self.compensation = total_error/(turns-2)

    def usDelay(self,delayInUs):
       period = delayInUs - self.compensation   
       if period >0: 
           self.libc.usleep(int(period))
