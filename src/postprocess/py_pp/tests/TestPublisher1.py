from MyPublisher import MyPublisher
import time
import json

if __name__ == "__main__":
    test = MyPublisher("TestPublisher1")
    test.start()

    a = 0
    while (a < 20):
        timenow = time.ctime()
        payload = {"chat_ID": 123456, "location": {"latitude": 45.03, "longitude": 7.62}, "status": "closed", "timestamp": str(timenow)}
        print("Publishing: '%s'" % (payload))
        test.mqtt_client.myPublish("/Turin/notifications/u1", json.dumps(payload))   
        a += 1
        time.sleep(1)

    test.stop()
