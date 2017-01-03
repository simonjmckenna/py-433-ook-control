#!/usr/bin/python3

# File to handle Energenie protocol specics 

# The address is 20 bits

addresslen=20
buttonlen=3
onofflen=1
stoplen=1

class EnergenieProtocol():
    initialised=0
    address="10101010101010101010"
    stop="1"
    ON="1"
    OFF="0"
    BUTTON1="111"
    BUTTON2="011"
    BUTTON3="101"
    BUTTON4="001"
    BUTTONA="110"

    def __init(self):
        initialised =1

    def build_frame(self,address,button,onoff):
        if address == None:
           address = self.address
        bitstream = address + button + onoff + self.stop
        return bitstream

    def generate_address(self,addressid):
        addressval=addressid
        self.address = 0
        while addressval > 0:
            if addressval % 2 == 1:
               self.address = "1" + self.address
            else:
               self.address = "0" + self.address
            addressval = addressval // 2
        return address

# frame_delay=10000
# zero_pulse_width = 320
# one_pulse_width = 1020
# bit_width = 1400

