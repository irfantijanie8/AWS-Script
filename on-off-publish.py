# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

import RPi.GPIO as GPIO

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a25u505gryt1a7-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "../cert/c5a0d6e9ca9ccff70dd905abf209ad79a1d5b1fec70dd8205e23529bb128551f-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "../cert/c5a0d6e9ca9ccff70dd905abf209ad79a1d5b1fec70dd8205e23529bb128551f-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "../cert/root.pem"
MESSAGE = "Hello World"
TOPIC = "test/testing"
RANGE = 20

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')

try:
    message = {"message" : "Machine Off", "led_state": "Led Off"}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    state = False
    while True:
            #GPIO.output(24, True)
            if(not state):
                data = "Machine On"
                led_state = "Led On"
                state = True
            else:
                data = "Machine Off"
                led_state = "Led Off"
                state = False
            message = {"message" : data, "led_state": led_state}
            mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
            t.sleep(1)
        
except KeyboardInterrupt:
    print('interrupted!')
    print('Publish End')
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()