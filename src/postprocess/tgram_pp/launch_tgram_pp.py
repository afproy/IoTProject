"""
PostProcess Engine for Telegram:

Main script to be run to make the postprocess engine operational.
It instantiates a CityManager, starts it, subscribes to the notifications topic
and waits until Ctrl+'C' is pressed.
"""

from engine.CityManager import CityManager
import time


if __name__ == "__main__":

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
