#!/usr/bin/python

import energenie433

t_address="a" *20
t_button="b" *3
t_onoff="o"

CONFIGFILE="eg_config"

testval=255

failed_tot = 0
failed     = 0

print("TEST START - Energenie Protocol ")

egp = energenie433.EnergenieProtocol()

#
# Protocol Frame tests
#
address = egp.encode_address(testval)
value   = egp.decode_address(address)

if value != testval:
   print("Failed address encode/deode value {} for address {}".format(value,address))
   failed +=1


frame = egp.build_frame(t_address,t_button,t_onoff)
packet= egp.decode_frame(frame)

print("address:",packet["address"])
if packet["address"] != t_address:
    print("ADDRESS frame encode/decode failed");
    failed += 1

print("button :",packet["button"])
if packet["button"] != t_button:
    print("BUTTON frame encode/decode failed");
    failed += 1

print("onoff  :",packet["onoff"])
if packet["onoff"] != t_onoff:
    print("ONOFF frame encode/decode failed");
    failed += 1

if failed != 0:
    print("FAILED - Protocol Frame tests failures {}".format(failed))
    failed_tot += failed
    failed =0
else:
    print("SUCCESS - Passed Protocol Frame Tests")

#
# Device Config tests
#
address = egp.encode_address(1024)

result = egp.load_defaults()
if result != egp.radio.VALID_ALL:
   print("Failed to load protocol defaults return [{}]".format(result))
   failed += 1

result = egp.load_new_device("plug1",address,egp.BUTTON1)
if result != "plug1":
   print("FAILED Failed to create device plug1")
   failed += 1
result = egp.load_new_device("plug2",address,egp.BUTTON2)
if result != "plug2":
   print("FAILED Failed to create device plug2")
   failed += 1
result = egp.load_new_device("plug3",address,egp.BUTTON3)
if result != "plug3":
   print("FAILED Failed to create device plug3")
   failed += 1
result = egp.load_new_device("plug3",address,egp.BUTTON3)
if result == "plug3":
   print("FAILED Managed to recreate device plug3")
   failed += 1

result = egp.save_configuration(CONFIGFILE)

if failed != 0:
    print("FAILED - Device Config tests failures {}".format(failed))
    failed_tot += failed
    failed =0
else:
    print("SUCCESS - Passed Device config Tests")
#
# Device Trasnmit tests
#
result = egp.turnon_device("plug1")
if result != True:
   print("FAILED Failed to turn on device plug1")
   failed += 1
result = egp.turnon_device("plug2")
if result != True:
   print("FAILED Failed to turn on device plug2")
   failed += 1
result = egp.turnon_device("plug3")
if result != True:
   print("FAILED Failed to turn on device plug3")
   failed += 1

result = egp.turnoff_device("plug1")
if result != True:
   print("FAILED Failed to turn off device plug1")
   failed += 1
result = egp.turnoff_device("plug2")
if result != True:
   print("FAILED Failed to turn off device plug2")
   failed += 1
result = egp.turnoff_device("plug3")
if result != True:
   print("FAILED Failed to turn off device plug3")
   failed += 1

result = egp.turnon_device("plug4")
if result == True:
   print("FAILED tried to turn on bad device plug4")
   failed += 1
result = egp.turnon_device("plug4")
if result == True:
   print("FAILED tried to turn off bad device plug4")
   failed += 1

if failed != 0:
    print("FAILED - Device transmit tests failures {}".format(failed))
    failed_tot += failed
    failed =0
else:
    print("SUCCESS - Passed Device Transmit Tests")

egp.load_configuration(CONFIGFILE)

