#!/usr/bin/python

import hrSleep, time

def doSleeping():
    for period in range(1,10):
        start = time.time() 
        slp.usDelay(int(period*100))
        delay = time.time() - start
        print "Delay asked for"+str(period*100)+"us - Got "+str(delay*1e6)+"us"
  
slp = hrSleep.hrSleep()

doSleeping()

slp.SetCompensation(200,1000)
print "compensation ="+str(slp.compensation)

doSleeping()

slp.clearCompensation()
doSleeping()

