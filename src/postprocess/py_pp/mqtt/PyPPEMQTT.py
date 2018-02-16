import paho.mqtt.client as MQTT

class PyPPEMQTT:
    """ Class PyPPEMQTT:

    It is the Python PostProcess Engine MQTT subscriber. It is through an
    instance of this class that the postprocess engine is able to receive the
    messages from the broker that are necessary to manage the city and send
    notifications to users.

    Use the methods in this order:
    1) start()
    2) mySubscribe(...)
    3) stop()

    Attributes:
        clientID: represents the ID of the city, "Turin" for example
        broker (str): URL of the broker used
        port (int): port of the broker used
        topic (str): topic to subscribe to
        notifier (:obj: CityManager.notifier): reference of the method to call
            upon reception of a message
        py_ppe_mqtt_client (:obj: MQTT.Client): MQTT client of the subscriber
    """


    def __init__(self, clientID, broker, port, notifier):
        """ Constructor of PyPPEMQTT:

        Initializes all the attributes of the subscriber and instantiates a
        MQTT client. It also registers all the necessary callbacks of the
        MQTT client.

        Args:
            clientID: represents the ID of the city, "Turin" for example
            broker (str): URL of the broker used
            port (int): port of the broker used
            notifier (:obj: CityManager.notifier): reference of the method to
                call upon reception of a message
        """
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.clientID = clientID

        self.topic = ""

        # create an instance of paho.mqtt.client
        self.py_ppe_mqtt_client = MQTT.Client(clientID, False) 

        # register the callback
        self.py_ppe_mqtt_client.on_connect = self.myOnConnect
        self.py_ppe_mqtt_client.on_disconnect = self.myOnDisconnect
        self.py_ppe_mqtt_client.on_message = self.myOnMessage


    def myOnConnect(self, mqtt_client, userdata, flags, rc):
        """ myOnConnect function called by on_connect callback:
        
        Called upon connection to the broker. Everything goes well if rc == 0
        otherwise we have some connection issues with the broker. If so it is
        printed in the terminal and the CityManager is notified so that it can
        shut down.

        Args:
            mqtt_client (:obj: MQTT.Client): client instance of the callback
            userdata (str): user data as set in Client (not used here)
            flags (int): flag to notify if the user's session is still
                available (not used here)
            rc (int): result code
        """
        errMsg = ""

        if rc == 0:
            print("PyPPEngine successfully connected to broker!")
            return

        # If we go through this we had a problem with the connection phase
        elif 0 < rc <= 5:
            errMsg = "/!\ PyPPEngine connection to broker was refused" \
                     " because of: "
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
            errMsg = "/!\ PyPPEngine connection to broker was refused for" \
                     " unknown reasons!"
        print(errMsg)
        # Stopping the loop
        self.py_ppe_mqtt_client.loop_stop()

        # Notifying the CityManager
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
            print("PyPPEngine successfully disconnected!")
        else:
            print("Unexpected disconnection of PyPPEngine!" \
                  " Reconnecting right away!")
            # The reconnection is performed automatically by our client since
            # we're using loop_start() so no need to manually tell our client
            # to reconnect.


    def myOnMessage(self, mqtt_client, userdata, msg):
        """ myOnMessage function called by on_message callback:

        Our subscriber has received a message and therefore, it notifies the
        CityManager.

        Args:
            mqtt_client (:obj: MQTT.Client): client instance of the callback
            userdata (str): user data as set in Client (not used here)
            msg (:obj: MQTTMessage): message sent by the broker
        """
        # A new message is received
        self.notifier.notify(False, msg.topic, msg.payload.decode("utf-8", \
                                                                  "ignore"))


    def mySubscribe(self, topic, qos = 2):
        """ mySubscribe:
        
        Method that allows to subscribe to a specific topic with a particular
        QoS, by default it's 2.

        Args:
            topic (str): topic to which you desire to subscribe
            qos (int): desired QoS
        """
        print("PyPPEngine subscribing to %s" % (topic))
        # Subscribing to a topic
        self.py_ppe_mqtt_client.subscribe(topic, qos)
        self.topic = topic


    def start(self):
        """ start:

        Starts the subscriber by connecting to the broker and starting the loop
        necessary to receive messages from the broker.
        """
        # Connecting our client to the broker
        self.py_ppe_mqtt_client.connect(self.broker , self.port)
        # Starting the loop to start receiving messages from the broker
        self.py_ppe_mqtt_client.loop_start()


    def stop(self):
        """ stop:

        Stops the subscriber by unsubscribing from the topic, stopping the loop,
        disconnecting from the broker
        """
        # Unsubscribing from topic
        self.py_ppe_mqtt_client.unsubscribe(self.topic)
        # Stopping the loop
        self.py_ppe_mqtt_client.loop_stop()
        # Finaly, disconnecting the client from the broker
        self.py_ppe_mqtt_client.disconnect()