"""
Script to launch our Telegram bot microservice:

Main script to be run to make our Telegram bot operational.
It instantiates a BotManager, starts it, subscribes to the topic to which the
associated Python postprocess engine will publish notifications and waits until
Ctrl+'C' is pressed.
"""

from bot.BotManager import BotManager
import time
import requests
import json
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \
                                            './../../catalog/')))
from classes import IamAlive
from util import *

if __name__ == '__main__':

    # Loading configuration file
    conf = json.load(open("conf.json", "r"))

    # 1) Perform registration to catalog by creating dedicated thread
    registration(conf)

    # 2) Retrieve information regarding broker
    broker_host, broker_port = getBroker(conf)

    # 3) Ask for information about next actor

    try:
        topic = conf["catalog"]["registration"]["expected_payload"] \
                    ["requirements"]["topics"][0]
        myBotManager = BotManager(broker_host, broker_port)
        myBotManager.manage()
        myBotManager.myMqttClient.mySubscribe(topic)

        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        myBotManager.rest()
