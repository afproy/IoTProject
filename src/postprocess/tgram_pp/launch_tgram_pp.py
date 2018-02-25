"""
PostProcess Engine for Telegram:

Main script to be run to make the postprocess engine operational.
It instantiates a CityManager, starts it, subscribes to the notifications topic
and waits until Ctrl+'C' is pressed.
"""

from engine.CityManager import CityManager
import time
import requests
import json
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \
                                            './../../catalog/')))
from classes import IamAlive

if __name__ == "__main__":

    # Loading configuration file
    conf = json.load(open("conf.json", "r"))

    # Retrieving catalog URL to register to it
    url = conf["catalog"]["URL"]
    # Retrieving the payload expected by the catalog
    payload = conf["catalog"]["expected_payload"]
    # Retrieving the interval of time at which our actor should communicate
    # with the catalog
    interval = conf["catalog"]["interval"]
    
    # Starting to send registration messages to catalog
    IamAlive(url, payload, interval)

    try:
        # Creating a CityManager for turin with the coordinates of a NW point
        # and of a SE point, it will be composed of 4*4 Neighborhood and the
        # threshold of open umbrellas per neighborhood after which a rain
        # warning is sent is set to 2
        TurinManager = CityManager("Turin", 45.106234, 7.619275, 45.024758, 7.719869, 4, 2)
        TurinManager.manage()
        TurinManager.myPyPPEMqttClient.mySubscribe("/Turin/+/notifications")

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        TurinManager.rest()
