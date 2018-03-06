import paho.mqtt.client as MQTT
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class OurMQTT:
    """ Class OurMQTT:

    It is a general purpose MQTT client class, can be used to implement either
    MQTT subscribers or publishers.

    Use the methods in this order:
    1) start()
    2) mySubscribe(...)
    3) stop()

    Attributes:
        clientID: represents the ID of the MQTT client
        broker (str): URL of the broker used
        port (int): port of the broker used
        topic (str): topic to subscribe to
        notifier (:obj: notifier): reference of the object on which to call the
            notify() method upon reception of a message
        mqtt_client (:obj: MQTT.Client): MQTT client
    """


    def __init__(self, clientID, broker, port, notifier):
        """ Constructor of OurMQTT:

        Initializes all the attributes of our client and instantiates a
        MQTT client. It also registers all the necessary callbacks of the
        MQTT client.

        Args:
            clientID: represents the ID of the MQTT client
            broker (str): URL of the broker used
            port (int): port of the broker used
            notifier (:obj: notifier): reference of the method to call upon
                reception of a message
        """
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID

        self.topic = ""
        self.isSubscriber = False

        # create an instance of paho.mqtt.client
        self.mqtt_client = MQTT.Client(clientID, False) 

        # register the callback
        self.mqtt_client.on_connect = self.myOnConnect
        self.mqtt_client.on_disconnect = self.myOnDisconnect
        self.mqtt_client.on_message = self.myOnMessage
        logger.info("Initiating MQTT client %s!" % (self.clientID))


    def myOnConnect(self, mqtt_client, userdata, flags, rc):
        """ myOnConnect function called by on_connect callback:
        
        Called upon connection to the broker. Everything goes well if rc == 0
        otherwise we have some connection issues with the broker. If so it is
        printed in the terminal and the notify() method of the notifier is
        called so that an appropriate action can be taken.

        Args:
            mqtt_client (:obj: MQTT.Client): client instance of the callback
            userdata (str): user data as set in Client (not used here)
            flags (int): flag to notify if the user's session is still
                available (not used here)
            rc (int): result code
        """
        errMsg = ""

        if rc == 0:
            logger.info("MQTT client %s successfully connected to broker!" \
                        % (self.clientID))
            return

        # If we go through this we had a problem with the connection phase
        elif 0 < rc <= 5:
            errMsg = "/!\ " + self.clientID + " connection to broker was " \
                     "refused because of: "
            if rc == 1:
                errMsg.append("the use of an incorrect protocol version!")
            elif rc == 2:
                errMsg.append("the use of an invalid client identifier!")
            elif rc == 3:
                errMsg.append("the server is unavailable!")
            elif rc == 4:
                errMsg.append("the use of a bad username or password!")
            else:
                errMsg.append("it was not authorised!")
        else:
            errMsg = "/!\ " + self.clientID + " connection to broker was " \
                     "refused for unknown reasons!"
        logger.error(errMsg)

        # Stopping the loop
        self.mqtt_client.loop_stop()

        # Notifying the notifier
        self.notifier.notify(True, "connection", errMsg)


    def myOnDisconnect(self, mqtt_client, userdata, rc):
        """ myOnDisconnect function called by on_disconnect callback:

        Can be triggered in one of two cases:
        - in response to a disconnect(): normal case, it was asked
        - in response to an unexpected disconnection: in that case the client
        will try to reconnect

        In both cases we log it.

        Args:
            mqtt_client (:obj: MQTT.Client): client instance of the callback
            userdata (str): user data as set in Client (not used here)
            rc (int): result code
        """
        if rc == 0:
            logger.info("MQTT client %s successfully disconnected!" \
                        % (self.clientID))
        else:
            logger.warning("Unexpected disconnection of MQTT client %s. " \
                           "Reconnecting right away!" % (self.clientID))
            # The reconnection is performed automatically by our client since
            # we're using loop_start() so no need to manually tell our client
            # to reconnect.


    def myOnMessage(self, mqtt_client, userdata, msg):
        """ myOnMessage function called by on_message callback:

        Our subscriber has received a message and therefore, it notifies the
        notifier.

        Args:
            mqtt_client (:obj: MQTT.Client): client instance of the callback
            userdata (str): user data as set in Client (not used here)
            msg (:obj: MQTTMessage): message sent by the broker
        """
        # A new message is received
        logger.info("MQTT client %s received a message:\n--%s,\n--on topic:" \
                    "\n--%s." % (self.clientID, msg.payload, msg.topic))
        self.notifier.notify(False, msg.topic, msg.payload.decode("utf-8", \
                                                                  "ignore"))


    def myPublish (self, topic, msg, qos = 2):
        """ myPublish:

        Method that makes the MQTT client publish to the the broker a message
        under a specific topic and with a particular QoS, which by default is 2.

        Args:
            topic (str): topic to which you desire to publish
            msg (str): message you wish to publish
            qos (int, optional): desired QoS, default to 2
        """
        logger.info("MQTT client %s publishing %s with topic %s."\
                    % (self.clientID, msg, topic))
        # publish a message with a certain topic
        self.mqtt_client.publish(topic, msg, qos)


    def mySubscribe(self, topic, qos = 2):
        """ mySubscribe:
        
        Method that allows to subscribe to a specific topic with a particular
        QoS, by default it's 2.

        Args:
            topic (str): topic to which you desire to subscribe
            qos (int, optional): desired QoS, default to 2
        """
        # Subscribing to a topic
        self.mqtt_client.subscribe(topic, qos)
        logger.info("MQTT client %s subscribed to %s." % (self.clientID, topic))
        # Remembering that our client is a subscriber
        self.isSubscriber = True
        self.topic = topic


    def start(self):
        """ start:

        Starts our client by connecting to the broker and starting the loop
        necessary to receive messages from the broker.
        """
        # Connecting our client to the broker
        self.mqtt_client.connect(self.broker , self.port)
        # Starting the loop to start receiving messages from the broker
        self.mqtt_client.loop_start()
        logger.info("MQTT client %s is now operational!" % (self.clientID))


    def stop(self):
        """ stop:

        Stops our client by unsubscribing from the topic (if our client is a
        subscriber), stopping the loop, and disconnecting from the broker.
        """
        if self.isSubscriber:
            # Unsubscribing from topic
            self.mqtt_client.unsubscribe(self.topic)
            logger.info("MQTT client %s unsubscribed from topic %s." \
                        % (self.clientID, self.topic))

        # Stopping the loop
        self.mqtt_client.loop_stop()
        # Finaly, disconnecting the client from the broker
        self.mqtt_client.disconnect()
        logger.info("MQTT client %s has correctly shut down!" % (self.clientID))