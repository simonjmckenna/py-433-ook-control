#!/usr/bin/env python3

import py433OOKControl


ook433a=py433OOKControl.ook433Control()
ook433b=py433OOKControl.ook433Control()

rxpin = 99
txpin = 98
if ook433a.set_rx_gpio_pin(rxpin) == None: print("failed to set RX GPIO pin to",rxpin)
if ook433a.set_tx_gpio_pin(txpin) == None:
   print("failed to set TX GPIO pin to",txpin)

rxpin = 17
txpin = 22

if ook433a.set_rx_gpio_pin(rxpin) == None:
   print("failed to set GPIO pin to",rxpin)

if ook433a.set_tx_gpio_pin(txpin) == None:
   print("failed to set GPIO pin to",txpin)

print("gpio rx pin is ",ook433a.get_rx_gpio_pin())
print("gpio tx pin is ",ook433a.get_tx_gpio_pin())

ook433a.define_device("plug1","plug1-on","plug1-off")
ook433a.define_device("plug2","plug2-on","plug2-off")
ook433a.define_device("plug3","plug3-on","plug3-off")

configfile="./433_config_a"
ook433a.write_config(configfile)
ook433b.read_config(configfile)
configfile="./433_config_b"
ook433a.write_config(configfile)
