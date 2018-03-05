from MyPublisher import MyPublisher
import time
import json

def openFirst16Umbrellas(mqtt_client, neighborhoods):
    for i in range(16):
        timenow = time.ctime()
        payload = {"chat_ID": i,                 \
                   "location": neighborhoods[i], \
                   "status": "open",             \
                   "timestamp": str(timenow)}
        topic = "/Turin/" + str(i) + "/notifications"
        mqtt_client.myPublish(topic, json.dumps(payload))
        print("Publishing: '%s'" % (payload))
        time.sleep(0.5)

def manageNext16Umbrellas(mqtt_client, neighborhoods, status):
    for i in range(16):
        timenow = time.ctime()
        payload = {"chat_ID": i+16,              \
                   "location": neighborhoods[i], \
                   "status": status,             \
                   "timestamp": str(timenow)}
        topic = "/Turin/" + str(i+16) + "/notifications"
        mqtt_client.myPublish(topic, json.dumps(payload))
        print("Publishing: '%s'" % (payload))
        time.sleep(0.5)

if __name__ == "__main__":
    test = MyPublisher("DemoScript")
    test.start()

    neighborhoods = json.load(open("demo_neighborhoods.json", "r"))
    neighborhoods = neighborhoods["neighborhoods"]

    openFirst16Umbrellas(test.mqtt_client, neighborhoods)

    print("\n\n\nWelcome to the demo! Umbrellas 0 to 15 have been placed in " \
          "each of the 16 neighborhoods composing the grid that represents "  \
          "Turin. You can now play with the following commands:\n- '0' to "   \
          "close umbrellas 16 to 31,\n- '1' to open them,\n- 'end' to end "   \
          "the demo.")
    endInput = input("\n> ")
    while endInput != "end":

        if endInput == '0':
            manageNext16Umbrellas(test.mqtt_client, neighborhoods, "closed")
        elif endInput == '1':
            manageNext16Umbrellas(test.mqtt_client, neighborhoods, "open")
        else:
            print("Incorrect command! Please use '0' to close umbrellas, " \
                  "'1' to open them or 'end' to end the demo.") 

        endInput = input("\n> ")

    test.stop()
