#---Update Mark
#Updates one mark based on player ID

#Operation: Update
#Collection: marks

def update_mark(mark, mongo):
    filter = {}
    options = {}
    filter['_id'] = mark['_id']
    try:
        result = mongo.connection.TMDB.marks.replace_one(filter, mark,upsert=True)
        return True
    except:
        txt_log.console("Exception in update_mark:" + str(filter), "error")
        return False