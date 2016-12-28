from datetime import datetime
import RPi.GPIO as GPIO
from parse import *


DefConfigFile = ".433ook-config"

# Class for 433 Mhz control - via RPi GPIO pins
class ook433Control():
    rpi_valid_gpio_pins=[4,5,6,7,8,12,13,16,17,18,19,20,22,23,24,25,27,29]
    gpio_rx_pin =0   # Pin to learn on
    gpio_tx_pin =0   # Pin to transmit on
    tx_dot_delay =0
    tx_dash_delay =0
    tx_frame_delay =0

    OOKdev_on={}
    OOKdev_off={}

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        init_run=True

    def set_tx_gpio_pin(self,txpin):
        #Check  it's a valid GPIO pin
        if txpin not in self.rpi_valid_gpio_pins:
           return None
        if self.gpio_tx_pin != 0:
           GPIO.cleanup(self.gpio_tx_pin)
        # Redefine the GPIO PIN to read from
        self.gpio_tx_pin = txpin
        GPIO.setup(TRANSMIT_PIN,txpin)
        return txpin

    def get_tx_gpio_pin(self):
        return self.gpio_tx_pin

    def get_rx_gpio_pin(self):
        return self.gpio_rx_pin

    def set_rx_gpio_pin(self,rxpin):
        #Check  it's a valid GPIO pin
        if rxpin not in self.rpi_valid_gpio_pins:
           return None
        if self.gpio_rx_pin != 0:
           GPIO.cleanup(self.gpio_rx_pin)
        # Redefine the GPIO PIN to read from
        self.gpio_rx_pin = rxpin
        GPIO.setup(RECIEVE_PIN,rxpin)
        return rxpin

    def listen():
        return None

    def transmit_ook(self,device,onoff):
        #Send a code to the transmitter
        if onoff ="ON":
           message=self.OOKdev_on[device] 
        else:
           message=self.OOKdev_on[device] 

        for thisgo in range(tx_cycles):
           for bit in message:
               if bit == '0':
                    GPIO.output(self.gpio_txpin, 1)
                    time.sleep(dot_delay)
                    GPIO.output(self.gpio_txpin, 0)
                    time.sleep(dash_delay)
               elif bit == '1':^M
                    GPIO.output(self.gpio_txpin, 1)
                    time.sleep(dash_delay)
                    GPIO.output(self.gpio_txpin, 0)
                    time.sleep(dot_delay)
               else:
                    continue
           # End of Message - tidy up before next one
           GPIO.output(self.gpio_txpin, 0)
           time.sleep(frame_delay)
           
        return None

    def define_device(self,name,oncode,offcode):
        #Load a new device and on and off code into the configuration
        self.OOKdev_on[name]=oncode
        self.OOKdev_off[name]=offcode
        return name   

        return None

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
               if self.set_rx_gpio_pin(int(result['value'])) == None:
                  return "bad "+result['item']+" value:"+result['value']
           elif result['item'] == "GPIO_TX_PIN":
               print("TX_PIN")
               if self.set_tx_gpio_pin(int(result['value'])) == None:
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
        result=parse("DELAY {type}={value}",line)
        if result != None:
           print("DELAY")
           self.define_delay(result['type'],result['value'])
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
        print("start writing file Devices")
        config.write("# Plug Groups Names and Codes\n")

        for device,oncode in self.OOKdev_on.items():
            offcode = self.OOKdev_off[device]
            config.write("DEVICE "+device+"="+oncode+","+offcode+"\n")
        config.write("#End Of File\n")
        print("Done writing file")
        config.close()


