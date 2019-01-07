#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
from gpiozero import Energenie

import io

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class SnipsEnergenie(object):
    
    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None
        
        # start listening to MQTT
        self.start_blocking()
    
    def master_callback(self, hermes, intent_message):
        if intent_message.intent.intent_name == 'pezholio:energenie_all_on':
            for i in range(1, 4):
                lamp = Energenie(i)
                lamp.on()
                lamp.on()
        elif intent_message.intent.intent_name == 'pezholio:energenie_all_off':
            for i in range(1, 4):
                lamp = Energenie(i)
                lamp.off()
                lamp.off()

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_callback).start()

if __name__ == "__main__":
    SnipsEnergenie()
    
