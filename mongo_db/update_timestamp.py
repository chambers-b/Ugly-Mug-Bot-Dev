#Updates the timestamp field to the current time for an entire faction

#Operation: Update
#Collection: marks

from ext import *  #Import external package set

def update_timestamp(faction_id, mongo):
    filter = {'faction':faction_id}
    options = {}
    ms = datetime.datetime.now()
    update = {'$set':{'last_update': time.mktime(ms.timetuple())}}
    
    start_time = time.mktime(ms.timetuple())
    result = mongo.connection.TMDB.marks.update_many(filter, update, upsert=True)
    return True
#except:     
    print("Exception in update_mark_collection:" + str(filter))
    return False  