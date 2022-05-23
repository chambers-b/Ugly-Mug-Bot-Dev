
#Operation: Update
#Collection: active_alerts

def update_message(message, mongo):
    filter = {}
    filter['_id'] = message['_id']
    try:
        result = mongo.connection.TMDB.active_alerts.update_one(filter, mark,upsert=True)
        return True
    except:
        txt_log.console("Exception in update_message:" + str(filter), "error")
        return False