import json
import requests
import reservations
import scheduler
import defects

def getData(body, url, date, type):
    try:
        r = requests.post(url, json=body)
        print('print response')
        text = r.content
        print(text)
        print("\n###########\n")
        data = json.loads(text)
        print(json.dumps(data, indent=4, sort_keys=True))
        return data   #parseData(data,type,date
    except:
        print("ples halp")
        # self.error(type) #TODO create error handling class

def parseData(data, type, date):
    if type == 0:
        for i in data:
            print("printing day:")
            print(str(date.day()))
            print(i["fields"]["date"][0:2] == str(date.day()))
            if i["fields"]["date"][0:2] == str(date.day()):
                reservations.enterReservation(int(i["fields"]["timeslotfrom"]), int(i["fields"]["timeslotto"]),
                                      " %s %s %s %s %s" % (str(i["fields"]["timefrom"]), str(i["fields"]["timeto"]),
                                                           str(i["fields"]["room"]), str(i["fields"]["lesson"]),
                                                           str(i["fields"]["username"])))
    elif type == 1:
        for i in data:
            defects.enterDefects(i["fields"]["description"], i["fields"]["handled"], i["fields"]["type"])
    elif type == 2:
        for i in data:
            if i["fields"]["date"][0:2] == str(date.day()):
                scheduler.enterScheduler(int(i["fields"]["timeslotfrom"]), int(i["fields"]["timeslotto"]),
                                    " %s %s %s %s %s" % (str(i["fields"]["timefrom"]), str(i["fields"]["timeto"]),
                                                         str(i["fields"]["room"]), str(i["fields"]["lesson"]),
                                                         str(i["fields"]["username"])))
