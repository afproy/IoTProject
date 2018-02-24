import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \
                                            './../../../mqtt/')))
from OurMQTT import OurMQTT
from bot.RainBot import RainBot
import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class BotManager:
    """Class BotManager:

    BotManager has both an instance of a MQTT client and of RainBot. This way
    when it receives a message from the postprocess engine to notify a user
    it will be able to let the bot know that it needs to send a specification
    to a certain chat_ID.

    Attributes:
        myMqttClient (:obj: `OurMQTT`): MQTT client that acts as a subscriber
        myRainBot (:obj: `RainBot`): the instance of RainBot that implements our
            Telegram bot
    """

    def __init__(self):
        """ Constructor of BotManager:

        Creates instances of OurMQTT client and of RainBot for the its
        attributes.
        """
        logger.info("Initiating BotManager!")
        self.myMqttClient = OurMQTT("BotManager", "iot.eclipse.org", \
                                    1883, self)
        self.myRainBot = RainBot()


    def manage(self):
        """ BotManager starts to operate:

        By starting its MQTT client and RainBot.
        """
        self.myMqttClient.start()
        self.myRainBot.start_bot()
        logger.info("BotManager now operating!")
    

    def rest(self):
        """ BotManager shuts down:

        By stopping the MQTT client and stopping the RainBot.
        """
        self.myMqttClient.stop()
        self.myRainBot.stop()
        logger.info("BotManager has shut down!")


    def notify(self, bError, topic, msg):
        """ Method through which BotManager is notified by its MQTT client:

        When it is notified, the payload is analyzed and if it properly
        identifies a chat and asks to notify the chat then RainBot is asked
        to notify the user whose chat_ID matches the one received in the
        payload.

        Args:
            bError (bool): True when there was an error on the MQTT client's
                side
            topic (str): can either be the cause of the error received or the
                topic of the message received. In the second case the topic
                would look like something like this:
                /_city_/_umbrellaID_/rainbot
            msg (str): can either be the error message or the message received.
                On the second case the message would look like something like
                this:
                {
                    "chat_ID": ID,
                    "notify": bool
                }
        """
        if bError:
            if topic == "connection":
                errMsg = "/!\ Connection error of BotManager's MQTT "\
                         "client: %s\nShutting down..." % (msg)
                logger.warning(errMsg)
                self.rest()
                sys.exit()
        else:
            logger.info("BotManager received new message:\n- Topic: %s\n" \
                        "- Message: %s" % (topic, msg))
            jsonMsg = json.loads(msg)
            if BotManager.msgComplete(jsonMsg):
                chat_ID = int(jsonMsg["chat_ID"])
                if jsonMsg["notify"]:
                    self.myRainBot.notify(chat_ID)
            else:
                logger.info("BotManager received a bad formatted message!")


    def msgComplete(msg):
        """ method to check whether the message received is complete:
        Args:
            msg (:obj: `dict` of :obj: `JSON`): json payload received
        """
        return ("chat_ID" in msg) and ("notify" in msg)
        