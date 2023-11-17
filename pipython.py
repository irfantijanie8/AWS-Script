import time
import paho.mqtt.client as mqtt
import ssl
import json
import thread
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./c5a0d6e9ca9ccff70dd905abf209ad79a1d5b1fec70dd8205e23529bb128551f-certificate.pem.crt', keyfile='./c5a0d6e9ca9ccff70dd905abf209ad79a1d5b1fec70dd8205e23529bb128551f-private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a25u505gryt1a7-ats.iot.us-east-1.amazonaws.com", 8883, 60) #Taken from REST API endpoint - Use your own. 


def intrusionDetector(Dummy):
    while (1):    
	x=GPIO.input(21)
        if (x==0): 
            print "Just Awesome" 
            client.publish("device/data", payload="Hello from BinaryUpdates!!" , qos=0, retain=False)
        time.sleep(5)

thread.start_new_thread(intrusionDetector,("Create intrusion Thread",))
    
client.loop_forever()