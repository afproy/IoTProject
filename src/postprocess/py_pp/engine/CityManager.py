from mqtt.PyPPEMQTT import PyPPEMQTT
from engine.space.City import City
import sys
import json

class CityManager:
    """ Class CityManager:

    Class in charge of managing a City. Has a MQTT subscriber which subscribes
    to a specific topic of interest for the city. Upon the reception of a
    message it triggers the update of the City. Which in turn triggers the
    notification of the user in case it is needed.

    Attributes:
        clientID (str): represents the ID of a city, 'Turin' for example
        myPyPPEMqttClient (:obj: PyPPEMQTT): MQTT client, implements a
            subscriber
        myCity (:obj: City): the City to manage
    """

    def __init__(self, clientID, nwLat, nwLong, seLat, seLong, n, threshold):
        """ Constructor of CityManager:

        Initializes the attributes of the class. To do so it creates an instance
        of a PyPPEMQTT client and an instance of a City.

        Args:
            clientID (str): of the city to manage
            nwLat (float): latitude of the North West point
            nwLong (float): longitude of the North West point
            seLat (float): latitude of the South East point
            seLong (float): longitude of the South East point
            n (int): square root of the wanted number of neighborhoods composing
                the city
            threshold (int): number of users with their umbrella opened in a
                Neighborhood at which a notification to the users with their
                umbrella closed need to be sent
        """
        self.clientID = clientID
        self.myPyPPEMqttClient = PyPPEMQTT(self.clientID, "iot.eclipse.org", \
                                           1883, self)
        self.myCity = City(self.clientID, nwLat, nwLong, seLat, seLong, n, \
                           threshold)


    def manage(self):
        """ CityManager starts to manage its city:

        By starting its MQTT client it allows it to receive the messages of the
        topic it has subscribed to.
        """
        print("Starting to manage %s's parc of umbrellas!" % (self.clientID))
        self.myPyPPEMqttClient.start()

    def rest(self):
        """ CityManager stops managing its city by stopping its MQTT client.
        """
        print("Finishing management of %s's parc of umbrellas!" % (self.clientID))
        self.myPyPPEMqttClient.stop()

    def notify(self, bError, topic, msg):
        """ Method through which CityManager is notified by its MQTT client:

        Args:
            bError (bool): True when there was an error on the MQTT client's
                side
            topic (str): can either be the cause of the error received or the
                topic of the message received. In the second case the topic
                would look like something like this:
                /city/notifications/_umbrellaID_
            msg (str): can either be the error message or the message received.
                On the second case the message would look like something like
                this:
                {
                    "chat_ID": ID,
                    "location":
                    {
                        "latitude": lat,
                        "longitude": long
                    },
                    "status": "s",
                    "timestamp": "ts
                }
        """
        if bError:
            if topic == "connection":
                print("/!\ Connection error of CityManager's MQTT client: %s" & (msg))
                print("Shutting down...")
                sys.exit()
        else:
            print("CityManager received the following message: %s" % (msg))