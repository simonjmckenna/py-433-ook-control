#!/usr/bin/python3
import py433OOKControl

# File to handle Energenie protocol specics 

# The address is 20 bits
addresslen=20
# 3 bits for the button
buttonlen=3
# 1 bit for on / off
onofflen=1
# 1 bit as a stop value
stoplen=1
# whole frame length
framelen = addresslen + buttonlen + onofflen + stoplen

class EnergenieProtocol():
    initialised=False
    address="10101010101010101010"
    STOP="1"
    ON="1"
    OFF="0"
    BUTTON1="111"
    BUTTON2="011"
    BUTTON3="101"
    BUTTON4="001"
    BUTTONA="110"
    radio  = py433OOKControl.ook433Control()

    # Init function
    def __init(self):
        self.radio.reinitialise()

    # Load the standard protocol defaults into the radio code 
    def load_defaults(self): 
        self.radio.reinitialise()
        # Frame_delay = 10000
        value=10000
        if self.radio.set_protocolTime(self.radio.FRAME,value) != value:
            return radio.FRAME
        # zero_pulse_width = 320
        value = 320
        if self.radio.set_protocolTime(self.radio.ZERO,value) != value:
            return self.radio.ZERO
        # one_pulse_width = 1020
        value = 1020
        if self.radio.set_protocolTime(self.radio.ONE,value) != value:
            return self.radio.ONE
        # bit_width = 1400
        value = 1400
        if self.radio.set_protocolTime(self.radio.BIT,value) != value:
            return self.radio.BIT
        # TX CYCLES = 10
        value = 10
        if self.radio.set_protocolTime(self.radio.TXCYCLES,value) != value:
            return self.radio.TXCYCLES
        # Set the GPIO TX PIN = 23
        value = 23
        if self.radio.set_tx_gpio_pin(value) != value:
            return self.radio.GPIO_TX
        # Set the GPIO RX PIN
        value = 22
        if self.radio.set_rx_gpio_pin(value) != value:
            return self.radio.GPIO_RX
        # Success - set flag and return ok
        if self.radio.is_initialised(self.radio.VALID_ALL) != True:
            return self.radio.VALID_NONE
        return self.radio.VALID_ALL

    # turn an address value into an address bitstream
    def encode_address(self,addressid):
        addressval=addressid
        if addressval > 2 << (addresslen+1):
            return None
        self.address = ""
        for count in range (0,addresslen):
            if addressval % 2 == 1:
               self.address = "1" + self.address
            else:
               self.address = "0" + self.address
            addressval = addressval // 2
        return self.address

    # turn an address bitstream into an address value
    def decode_address(self,address):
        value = 0
        power = addresslen -1 
        if len(address) -1 != power:
           return None
        for bit in address:
            if bit not in ["0", "1"]:
               return None 
            value += int(bit) << power  
            power -= 1

        return value

    # build a protocol frame from the components
    def build_frame(self,address,button,onoff):
        frame=""
        if address == None:
           address = self.address
        frame = address + button + onoff + self.STOP
        return frame

    # Break a frame up into it's constituent parts
    def decode_frame(self,frame):
        packet = {}
        if len(frame) != framelen:
           return None

        packet["address"]= frame[:20]
        packet["button"] = frame[20:23]
        packet["onoff"]  = frame[23:24]

        return packet

    # laod new device entries into the database
    def load_new_device(self,name,address,button):
        on_frame  =  self.build_frame(address,button,self.ON)
        if len(on_frame) != framelen:
            return None
        off_frame =  self.build_frame(address,button,self.OFF)
        if len(off_frame) != framelen:
            return None

        return self.radio.define_device(name,on_frame,off_frame)

    def turnon_device(self,name):
        if self.radio.is_initialised(self.radio.VALID_TX) != True:
           return False
        return self.radio.transmit_ook(name,self.radio.ON)

    def turnoff_device(self,name):
        if self.radio.is_initialised(self.radio.VALID_TX) != True:
           return False
        return self.radio.transmit_ook(name,self.radio.OFF)

    def listen_to_radio():
        if self.radio.is_initialised(self.radio.VALID_RX) != True:
           return None
        return self.radio.listen()

           
    def load_configuration(self,configfile):
        result = self.radio.read_config(configfile)

        return result

    def save_configuration(self,configfile):
         return self.radio.write_config(configfile)
