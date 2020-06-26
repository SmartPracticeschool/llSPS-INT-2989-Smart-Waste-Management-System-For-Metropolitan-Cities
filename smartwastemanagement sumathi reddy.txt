import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

#Provide your IBM Watson Device Credentials
organization = "py1o4z"
deviceType = "dustbin"
deviceId = "636912"
authMethod = "token"
authToken = "rohini6369"

client = Cloudant("28934080-e562-4a0f-89d4-632ca856f05e-bluemix", "c2fb9e1a7a8bf7cc45013ce5c1b8102cfba0d60bf5709f43ab623f262cd61e50", url="https://28934080-e562-4a0f-89d4-632ca856f05e-bluemix:c2fb9e1a7a8bf7cc45013ce5c1b8102cfba0d60bf5709f43ab623f262cd61e50@28934080-e562-4a0f-89d4-632ca856f05e-bluemix.cloudantnosqldb.appdomain.cloud")
client.connect()
database_name = "smartwastemanagement"
my_database = client.create_database(database_name)

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
        if L>90:
                x=requests.get("https://www.fast2sms.com/dev/bulk?authorization=PZ6y5KcWmYAegTSJxH7RwsCE1Dba8hqI4t0fQjV9pGlFMdBoOnO3Q9Ce8fRwpysHGDvUa7Mnx5tPmI1Y&sender_id=FSTSMS&message=your garbage is full&language=english&route=p&numbers=8712262318")
                print(x.text)
        time.sleep(2)
        deviceCli.commandCallback = myCommandCallback
        
        if my_database.exists():
           print(f"'{database_name}' successfully created.")
        sample_data = [
            [1, "one", "garbagelevel", 67],
            [2, "two", "garbageweight", 40],]    

# Create documents using the sample data.
# Go through each row in the array
        for document in sample_data:
   # Retrieve the fields in each row.
          L = document[0]
          F = document[1]
   
          json_document = {"Garbage Level":L ,"Garbage Weight":F}
     # Create a document using the Database API.
          new_document = my_database.create_document(json_document)
   # Check that the document exists in the database
          if new_document.exists():
               print(f"Document '{json_document}' successfully created.")   
        
# Disconnect the device and application from the cloud
deviceCli.disconnect()
        


            
