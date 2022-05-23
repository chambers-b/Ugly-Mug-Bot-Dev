#Get flight alerts landing in the next few minutes
from ext import *  #Import external package set

import txt_log

def get_flight_alerts(mongo):
    filter = {}
    options = {}
    player_list = {}
    #del mark['_id']
#try:
    minutes = glob.al['minutes_before_landing']
    seconds_forward = 60 * minutes
    ms = datetime.datetime.now()
    forward_time = time.mktime(ms.timetuple()) + seconds_forward
    result = mongo.connection.TMDB.active_alerts.find(filter)
    filter = {'landing_time': {'$lt': forward_time}, 'type': 'travel'}
    txt_log.console("get_flight_alerts Query: " + str(filter), "debug")
    result = mongo.connection.TMDB.active_alerts.find(filter)
    for alert in result:
            alert_dict[alert['_id']] = alert
    print(str(alert_dict))
    return alert_dict
#except:     
    print("Exception in get_flight_alerts")
    return False  