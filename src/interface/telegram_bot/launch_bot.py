"""
Script to launch our Telegram bot microservice:

Main script to be run to make our Telegram bot operational.
It instantiates a BotManager, starts it, subscribes to the topic to which the
associated Python postprocess engine will publish notifications and waits until
Ctrl+'C' is pressed.
"""

from bot.BotManager import BotManager
import time

if __name__ == '__main__':

    try:
        myBotManager = BotManager()
        myBotManager.manage()
        myBotManager.myMqttClient.mySubscribe("/Turin/+/rainbot")

        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        myBotManager.rest()
