import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "py1o4z"
deviceType = "dustbin"
deviceId = "636912"
authMethod = "token"
authToken = "rohini6369"
# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='covered':
                print("dustbin is covered")
        elif i=='uncovered':
                print("dustbin is uncovered")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)#.............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()


# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
while True:
        L = random.randint(0, 100);
        F = random.randint(0, 100);
        data = { 'garbagelevel' : L, 'garbageweight': F}
        #print data
        def myOnPublishCallback():
            print ("Published Your Garbage_Level = %s %%" % L, "Garbage_Weight = %s %%" % F, "to IBM Watson")

        success = deviceCli.publishEvent("event", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        
        time.sleep(2)
        deviceCli.commandCallback = myCommandCallback
        
       
# Disconnect the device and application from the cloud
deviceCli.disconnect()
        


            
