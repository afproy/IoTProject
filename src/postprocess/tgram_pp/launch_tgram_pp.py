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

from util import *
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # Loading configuration file
    conf = json.load(open("conf.json", "r"))

    # 1) Perform registration to catalog by creating dedicated thread
    registration(conf)

    # 2) Retrieve information regarding broker
    broker_host, broker_port = getBroker(conf)

    # 3) Ask for information about next actor
    next_actors = conf["catalog"]["next_actor"]["params"]
    next_actor_requirements = getNextActorRequirements(conf)

    if (len(next_actor_requirements) == len(next_actors)) and \
       (next_actors[0]["ID"] in next_actor_requirements):
        next_actor_requirements = next_actor_requirements[next_actors[0]["ID"]]
    else:
        logger.error("Error while getting next_actor_requirements!")

    try:
        # Creating a CityManager for turin with the coordinates of a NW point
        # and of a SE point, it will be composed of 4*4 Neighborhood and the
        # threshold of open umbrellas per neighborhood after which a rain
        # warning is sent is set to 2
        topic = conf["catalog"]["registration"]["expected_payload"] \
                    ["requirements"]["topics"][0]
        confCM = conf["CityManager"]
        coord = confCM["coordinates"]
        TurinManager = CityManager(confCM["name"], broker_host, broker_port, \
                                   next_actor_requirements, coord["nwLat"], \
                                   coord["nwLong"], coord["seLat"], \
                                   coord["seLong"], confCM["n"], \
                                   confCM["threshold"])
        TurinManager.manage()
        TurinManager.myPyPPEMqttClient.mySubscribe(topic)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        TurinManager.rest()
