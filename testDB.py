from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import random
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from getpass import getuser

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

user = getuser()
AllowedActions = ['both', 'publish', 'subscribe']
if user == "antoine" :
host = "a1botgu2gaco6r-ats.iot.us-west-2.amazonaws.com"
rootCAPath = "/home/antoine/certs/AmazonRootCA1.pem"
certificatePath = "/home/antoine/certs/device.pem.crt"
privateKeyPath = "/home/antoine/certs/private.pem.key"
    thingName = "pine64"
elif user == "felix" :
    host = "a2yo8d743hfkwh-ats.iot.us-west-2.amazonaws.com"
    rootCAPath = "/home/felix/aws/cle/AmazonRootCA1.pem"
    certificatePath = "/home/felix/aws/cle/device.pem.crt"
    privateKeyPath = "/home/felix/aws/cle/private.pem.key"
    thingName = "Pine"
port = 443
useWebsocket = False
topic = "iot/topic"
clientId = thingName


# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

while True:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    message = {}
    message["time"] = dt_string
    message["temp"] = random.randint(0,30000)
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(1)
