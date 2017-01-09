from datetime import datetime
from hrSleep import hrSleep
import RPi.GPIO as GPIO
from parse import *

hrtime = hrSleep()

DefConfigFile = ".433ook-config"

# Class for 433 Mhz control - via RPi GPIO pins
class ook433Control():
    rpi_valid_gpio_pins=[4,5,6,7,8,12,13,16,17,18,19,20,22,23,24,25,27,29]

    VALID_NONE=0
    ZERO=1
    ONE=2
    BIT=4
    FRAME=8
    TXCYCLES=16
    GPIO_RX=32
    GPIO_TX=64
    VALID_RX=63 
    VALID_TX=95
    VALID_ALL=127
    initialised = 0
    ON=0
    OFF=1

    gpio_rx_pin =0   # Pin to learn on
    gpio_tx_pin =0   # Pin to transmit on
    zero_pulse =0
    one_pulse =0
    bit_width =0 
    frame_gap =0
    tx_cycles =0

    OOKdev_on={}
    OOKdev_off={}

    def __init__(self):
        self.reinitialise()

    def is_initialised(self,init_type):
        if self.initialised == self.VALID_ALL:
            return True
        if self.initialised == init_type:
            return True
        return False

    def reinitialise(self):
        GPIO.setmode(GPIO.BCM)
        self.gpio_tx_pin =0
        self.gpio_rx_pin =0
        self.bit_width = 0
        self.frame_gap = 0
        self.zero_pulse = 0
        self.one_pulse = 0
        self.tx_cycles = 0
        self.initialised = self.VALID_NONE
        return True

    def set_tx_gpio_pin(self,txpin):
        #Check  it's a valid GPIO pin
        if txpin not in self.rpi_valid_gpio_pins:
           return None
        if self.gpio_tx_pin != 0:
           GPIO.cleanup(self.gpio_tx_pin)
        # Redefine the GPIO PIN to read from
        self.gpio_tx_pin = txpin
        GPIO.setup(txpin,GPIO.OUT)
        self.initialised += self.GPIO_TX
        return txpin

    def set_rx_gpio_pin(self,rxpin):
        #Check  it's a valid GPIO pin
        if rxpin not in self.rpi_valid_gpio_pins:
           return None
        if self.gpio_rx_pin != 0:
           GPIO.cleanup(self.gpio_rx_pin)
        # Redefine the GPIO PIN to read from
        self.gpio_rx_pin = rxpin
        GPIO.setup(rxpin,GPIO.IN)
        self.initialised += self.GPIO_RX
        return rxpin
    
    def get_tx_gpio_pin(self):
        return self.gpio_tx_pin

    def get_rx_gpio_pin(self):
        return self.gpio_rx_pin

    def set_protocolTime(self,type,protocoltime):
        #Check  it's a valid delay - must be greater than the short delay
        if type == self.BIT:
           self.bit_width = protocoltime
           self.initialised += self.BIT
        elif type == self.FRAME:
           self.frame_gap = protocoltime
           self.initialised += self.FRAME
        elif type == self.ZERO:
           self.zero_pulse = protocoltime
           self.initialised += self.ZERO
        elif type == self.ONE:
           self.one_pulse = protocoltime
           self.initialised += self.ONE
        elif type == self.TXCYCLES:
           self.tx_cycles = protocoltime
           self.initialised += self.TXCYCLES
        else:
          return None

        return protocoltime

    def get_protocolTime(self,type):
        #Check  it's a valid delay - must be greater than the short delay
        if type == self.BIT:
           protocoltime= self.bit_width
        elif type == self.FRAME:
           protocoltime = self.frame_gap
        elif type == self.ZERO:
           protocoltime = self.zero_pulse
        elif type == self.ONE:
           protocoltime = self.one_pulse
        elif type == self.TXCYCLES:
           protocoltime = self.tx_cycles
        else:
          return None

        return protocoltime


    def listen():
        if self.is_initialised(VALID_RX) != True:
            return None
        return None

    def transmit_ook(self,device,onoff):
        # Have all the transmit parmeters been set properly
        if self.is_initialised(self.VALID_TX) != True:
            return False
        # Find the right transmit data
        try:
            if onoff == self.ON:
                message=self.OOKdev_on[device] 
            elif onoff== self.OFF:
                message=self.OOKdev_on[device] 
            else:
                return False
        except:
            return False

        zero_wait = self.bit_width - self.zero_pulse
        one_wait = self.bit_width - self.one_pulse

        #Send the code to the transmitter
        for thisgo in range(self.tx_cycles):
           for bit in message:
               if bit == '0':
                    GPIO.output(self.gpio_tx_pin, 1)
                    hrtime.usDelay(self.zero_pulse)
                    GPIO.output(self.gpio_tx_pin, 0)
                    hrtime.usDelay(zero_wait)
               elif bit == '1':
                    GPIO.output(self.gpio_tx_pin, 1)
                    hrtime.usDelay(self.one_pulse)
                    GPIO.output(self.gpio_tx_pin, 0)
                    hrtime.usDelay(one_wait)
               else:
                    continue
           # End of Message - tidy up before next one
           GPIO.output(self.gpio_tx_pin, 0)
           hrtime.usDelay(self.frame_gap)
          
        return True

    def define_device(self,name,oncode,offcode):
        #Load a new device and on and off code into the configuration
        # if it exists - dont try to re-add
        # if name in self.OOKdev_on == True : - for some reason fails
        if self.OOKdev_on.get(name) != None :
            return None

        self.OOKdev_on[name]=oncode
        self.OOKdev_off[name]=offcode
        return name   

    def process_cfg_line(self,line):
        #Parse and process the line of config file
        print(line)
        # See if this is a comment

        result=parse("#{item}",line)
        if result != None:
           print("COMMENT")
           return None
        # See if this is a SET
        result=parse("SET {item}={value}",line)
        if result != None:
           print("SET")
           if result['item'] == "GPIO_RX_PIN":
               print("RX_PIN")
               if self.set_rx_gpio_pin(int(result['value'])) != int(result['value']):
                  return "bad "+result['item']+" value:"+result['value']
           elif result['item'] == "GPIO_TX_PIN":
               print("TX_PIN")
               if self.set_tx_gpio_pin(int(result['value'])) == int(result['value']):
                  return "bad "+result['item']+" value:"+result['value']
           else:
               return "invalid variable -"+result['item']
           return None
        # See if this is a DEVICE
        result=parse("DEVICE {item}={oncode},{offcode}",line)
        if result != None:
           print("DEVICE")
           self.define_device(result['item'],result['oncode'],result['offcode'])
           return None 
        result=parse("TIMING {type}={value}",line)
        if result != None:
           print("TIMING")
           if result['type'] == "FRAME":
              print ("FRAME")
              if self.set_protocolTime(self.FRAME,int(result["value"]))== None:
                 return "bad value SPACING "+result["type"]+" value - "+result["value]"]
           elif result['type'] == "ZERO":
              print ("ZERO")
              if self.set_protocolTime(self.ZERO,int(result["value"]))== None:
                 return "bad value SPACING "+result["type"]+" value - "+result["value]"]
           elif result['type'] == "ONE":
              print ("ONE")
              if self.set_protocolTime(self.ONE,int(result["value"]))== None:
                  return "bad value SPACING "+result["type"]+" value - "+result["value]"]
           elif result['type'] == "BIT":
              print ("BIT")
              if self.set_protocolTime(self.BIT,int(result["value"]))== None:
                  return "bad value SPACING "+result["type"]+" value - "+result["value]"]
           elif result['type'] == "TXCYCLES":
              print ("TXCYCLES")
              if self.set_protocolTime(self.TXCYCLES,int(result["value"]))== None:
                  return "bad value SPACING "+result["type"]+" value - "+result["value]"]
           else:
               return "Invalid TIMING type -"+result["type"]
            
           return None 
        # Unknown line 
        return "Unknown Directive"

    def read_config(self,configfile=DefConfigFile):
        try:
            config = open(configfile,"r")
        except IOError:
            return None
        lineno=1
        for line in config:
            result = self.process_cfg_line(line)
            if result != None :
                # Had an error - description is the return 
                print("ERROR:LINE{}:{}".format(lineno,result))
            lineno+=1
        config.close()
 

    def write_config(self,configfile=DefConfigFile):
        try:
            config = open(configfile,"w")
        except IOError:
            return None
        print("start writing file GPIO")
        config.write("#433 OOK Config file for py433OOKControl\n")
        config.write("#GPIO Headers\n")
        config.write("SET GPIO_RX_PIN="+str(self.gpio_rx_pin)+"\n")
        config.write("SET GPIO_TX_PIN="+str(self.gpio_tx_pin)+"\n")
        config.write("TIMING BIT="+str(self.bit_width)+"\n")
        config.write("TIMING FRAME="+str(self.frame_gap)+"\n")
        config.write("TIMING ZERO="+str(self.zero_pulse)+"\n")
        config.write("TIMING ONE="+str(self.one_pulse)+"\n")
        config.write("TIMING TXCYCLES="+str(self.tx_cycles)+"\n")
        print("start writing file Devices")
        config.write("# Plug Groups Names and Codes\n")

        for device,oncode in self.OOKdev_on.items():
            offcode = self.OOKdev_off[device]
            config.write("DEVICE "+device+"="+oncode+","+offcode+"\n")
        config.write("#End Of File\n")
        print("Done writing file")
        config.close()


