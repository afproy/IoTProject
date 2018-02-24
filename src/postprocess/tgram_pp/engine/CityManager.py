import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \
                                            './../../../mqtt/')))
from OurMQTT import OurMQTT
from engine.space.City import City
import json

class CityManager:
    """ Class CityManager:

    Class in charge of managing a City. Has a MQTT subscriber which subscribes
    to a specific topic of interest for the city. Upon the reception of a
    message it triggers the update of the City. Which in turn triggers the
    notification of the user in case it is needed.

    Attributes:
        clientID (str): represents the ID of a city, 'Turin' for example
        myPyPPEMqttClient (:obj: OurMQTT): MQTT client, will be used as a
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
        self.myPyPPEMqttClient = OurMQTT("PyPPEngine", "iot.eclipse.org", \
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
        print("Finishing management of %s's parc of umbrellas!" \
              %(self.clientID))
        self.myPyPPEMqttClient.stop()


    def notify(self, bError, topic, msg):
        """ Method through which CityManager is notified by its MQTT client:

        When it is notified, the payload is split into the fields that
        represents a user and then City's method updateUser() is called so that
        it updates the position and/or status of its users. In return it
        receives the list of users who need to receive a rain warning so that
        the CityManager can then notify the bot so it can send notifications to
        the concerne users.

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
                print("/!\ Connection error of CityManager's MQTT client: %s" \
                      % (msg))
                print("Shutting down...")
                sys.exit()
        else:
            print("------------")
            print("Topic: %s" % (topic))
            print("Message: %s" % (msg))
            jsonMsg = json.loads(msg)
            if CityManager.msgComplete(jsonMsg):
                chat_ID = jsonMsg["chat_ID"]
                location = jsonMsg["location"]
                status = jsonMsg["status"]
                if CityManager.locComplete(location):
                    latU = location["latitude"]
                    longU = location["longitude"]
                    usersToBeNotified = self.myCity.updateUser(chat_ID, latU, \
                                                       longU, status == "open")
                    if usersToBeNotified != None:
                        for u in usersToBeNotified:
                            self.notifyUser(u)
                    return
            print("Bad format of the JSON!")


    def notifyUser(self, user):
        """ method which notifies the bot:

        About the users concerned with a rain warning. For the moment it only
        prints that it is notifying the user.

        Args:
            user (:obj: `User`): user to notify
        """
        print("Notifying: %s" % (str(user)))
        topic = "/Turin/" + str(user.chat_ID) + "/rainbot"
        payload = {"chat_ID": user.chat_ID, "notify": True}
        self.myPyPPEMqttClient.myPublish(topic, json.dumps(payload))


    def msgComplete(msg):
        """ method to check whether the message received is complete
        Args:
            msg (:obj: `dict` of :obj: `JSON`): json payload received
        """
        return ("chat_ID" in msg) and ("location" in msg) and ("status" in msg)


    def locComplete(location):
        """ method to check whether the message received is complete
        Args:
            location (:obj: `dict` of :obj: `float`): location received in the
                json paylad
        """
        return ("latitude" in location) and ("longitude" in location)
