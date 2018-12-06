import os
import sys
import time
from bluepy import sensortag

#tag = sensortag.SensorTag('24:71:89:07:84:03')
tag = sensortag.SensorTag(str(sys.argv[1]))

count = 0
time.sleep(1.0)
tag.lightmeter.enable()
tag.humidity.enable()
while True:
        tag.waitForNotifications(1.0)
	os.system("mosquitto_pub -h localhost -t \'IoT-Gateway01/ble/status\' -m \'SensorTag Connected\'") 
        lightdata = tag.lightmeter.read()
        tempdata = tag.humidity.read()

        print lightdata 
	print tempdata[0]
	#print humidata[1]

	os.system("mosquitto_pub -h localhost -t \'IoT-Gateway01/ble/lightdata\' -m \'" + str(lightdata)+ "'") 
	os.system("mosquitto_pub -h localhost -t \'IoT-Gateway01/ble/tempdata\' -m \' " + str(tempdata[0])  + "\'") 

	if tempdata[0] > 30: 
		os.system("mosquitto_pub -h localhost -t \'IoT-Gateway01/notification\' -m \'Need watering'") 
		os.system("/home/root/oily/oily_lcddisplay Need_Watering") 
	
	count = count + 1

	time.sleep(1.0)

	if count >= 10:
		count = 0
		os.system("/home/root/update-google-M1-L6.sh " + str(tempdata[0]) + " " + str(lightdata))

tag.disconnect()
del tag

