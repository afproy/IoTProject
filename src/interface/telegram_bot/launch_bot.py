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

if __name__ == '__main__':

    # Loading configuration file
    conf = json.load(open("conf.json", "r"))

    # Retrieving catalog URL to register to it
    url = conf["catalog"]["URL"] + conf["catalog"]["registration"]["URI"]
    # Retrieving the payload expected by the catalog
    payload = conf["catalog"]["registration"]["expected_payload"]
    # Retrieving the interval of time at which our actor should communicate
    # with the catalog
    interval = conf["catalog"]["registration"]["interval"]

    # Starting to send registration messages to catalog
    IamAlive(url, payload, interval)

    try:
        topic = conf["catalog"]["registration"]["expected_payload"] \
                    ["requirements"]["topics"][0]
        myBotManager = BotManager()
        myBotManager.manage()
        myBotManager.myMqttClient.mySubscribe(topic)

        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        myBotManager.rest()
