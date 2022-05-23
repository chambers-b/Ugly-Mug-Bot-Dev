#Remove marks older than ['days_to_hold_data'] from congif.json

#Operation: Delete
#Collection: marks

from ext import *  #Import external package set
import glob
import txt_log

def rm_old_marks(mongo):
    
    days = glob.al['days_to_hold_data']
    seconds_back = 60 * 60 * 24 * days
    ms = datetime.datetime.now()
    prev_time = time.mktime(ms.timetuple()) - seconds_back
    filter = {'last_update': {'$lt': prev_time}}
    txt_log.console("rm_old_marks Query: " + str(filter), "debug")
    try:
        result = mongo.connection.TMDB.marks.delete_many(filter)
        if result.acknowledged:
            return result.deleted_count    
    except:
        return "Exception: mongo_db.rm_old_marks (unknown response from database)"