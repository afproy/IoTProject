from MyPublisher import MyPublisher
import time
import json

if __name__ == "__main__":
    test = MyPublisher("MyPublisher")
    test.start()

    endInput = '1'
    while endInput != "end":
        timenow = time.ctime()
        payload = {}
        if endInput == '1':
            payload = {"chat_ID": 1, "location": {"latitude": 45.03, "longitude": 7.62}, "status": "closed", "timestamp": str(timenow)}
            test.myPublish("/Turin/notifications/u1", json.dumps(payload))
        elif endInput == '2':
            payload = {"chat_ID": 1, "location": {"latitude": 45.03, "longitude": 7.62}, "status": "open", "timestamp": str(timenow)}
            test.myPublish("/Turin/notifications/u1", json.dumps(payload))
        elif endInput == '3':
            payload = {"chat_ID": 1, "location": {"latitude": 45.08, "longitude": 7.68}, "status": "open", "timestamp": str(timenow)}
            test.myPublish("/Turin/notifications/u1", json.dumps(payload))
        elif endInput == '4':
            payload = {"chat_ID": 2, "location": {"latitude": 45.03, "longitude": 7.62}, "status": "open", "timestamp": str(timenow)}
            test.myPublish("/Turin/notifications/u2", json.dumps(payload))
        elif endInput == '5':
            payload = {"chat_ID": 2, "location": {"latitude": 45.03, "longitude": 7.62}, "status": "closed", "timestamp": str(timenow)}
            test.myPublish("/Turin/notifications/u2", json.dumps(payload))
        elif endInput == '6':
            payload = {"chat_ID": 3, "location": {"latitude": 45.03, "longitude": 7.62}, "status": "closed", "timestamp": str(timenow)}
            test.myPublish("/Turin/notifications/u2", json.dumps(payload))
        else:
            payload = {"invalid": True}
            test.myPublish("/Turin/notifications/", json.dumps(payload)) 

        print("Publishing: '%s'" % (payload))  
        endInput = input()

    test.stop()
