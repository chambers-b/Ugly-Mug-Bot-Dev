#Deletes an entry from the message collection
#Need to rework this

#Operation: Delete
#Collection: active_alerts

def rm_message(message, mongo):
    filter = {}
    filter['_id'] = message['_id']
    try:
        result = mongo.connection.TMDB.active_alerts.delete_many(filter)
        return True
    except:
        txt_log.console("Exception in rm_message:" + str(filter), "error")
        return False    