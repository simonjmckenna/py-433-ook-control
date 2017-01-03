#!/usr/bin/env python3

import py433OOKControl


Failed = 0

ook433a=py433OOKControl.ook433Control()
ook433b=py433OOKControl.ook433Control()

rxpin = 99
txpin = 98

if ook433a.set_rx_gpio_pin(rxpin) == None: 
   print("Success failed to set RX GPIO pin to",rxpin)
else:
   Failed += 1

if ook433a.set_tx_gpio_pin(txpin) == None:
   print("Success failed to set TX GPIO pin to",txpin)
else:
   Failed += 1

rxpin = 17
txpin = 22

if ook433a.set_rx_gpio_pin(rxpin) == None:
   Failed += 1
   print("failed to set GPIO pin to",rxpin)

if ook433a.set_tx_gpio_pin(txpin) == None:
   Failed += 1
   print("failed to set GPIO pin to",txpin)

if ook433a.get_rx_gpio_pin() != rxpin :
    Failed += 1
    print("gpio rx pin failed ",ook433a.get_rx_gpio_pin())

if ook433a.get_tx_gpio_pin() != txpin :
    Failed += 1
    print("gpio tx pin failed ",ook433a.get_tx_gpio_pin())

if ook433a.set_protocolTime(ook433a.ONE,30) != 30:
   Failed += 1
   print("set_protocolTime - ONE - failed")

if ook433a.set_protocolTime(ook433a.ZERO,15) != 15:
   Failed += 1
   print("set_protocolTime - ZERO - failed")

if ook433a.set_protocolTime(ook433a.BIT,60) != 60:
   Failed += 1
   print("set_protocolTime - BIT - failed")

if ook433a.set_protocolTime(ook433a.FRAME,1000) != 1000:
   Failed += 1
   print("set_protocolTime - FRAME - failed")

ook433a.define_device("plug1","plug1-on","plug1-off")
ook433a.define_device("plug2","plug2-on","plug2-off")
ook433a.define_device("plug3","plug3-on","plug3-off")

configfile="./433_config_a"
ook433a.write_config(configfile)
ook433b.read_config(configfile)
configfile="./433_config_b"
ook433a.write_config(configfile)

if ook433a.get_protocolTime(ook433a.FRAME) != ook433b.get_protocolTime(ook433b.FRAME):
   print("FRAME GAP")
   Failed += 1

if ook433a.get_protocolTime(ook433a.BIT) != ook433b.get_protocolTime(ook433b.BIT):
   print("BIT WIDTH")
   Failed += 1

if ook433a.get_protocolTime(ook433a.ZERO) != ook433b.get_protocolTime(ook433b.ZERO):
   print("ZERO PULSE")
   Failed += 1

if ook433a.get_protocolTime(ook433a.ONE) != ook433b.get_protocolTime(ook433b.ONE):
   print("ONE PULSE")
   Failed += 1

if ook433a.get_rx_gpio_pin() != ook433b.get_rx_gpio_pin() :
   print("get rx gpio pin")
   Failed += 1

if ook433a.get_tx_gpio_pin() != ook433b.get_tx_gpio_pin() :
   print("get tx gpio pin")
   Failed += 1

print("Failure count = "+str(Failed))
