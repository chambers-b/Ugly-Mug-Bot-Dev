#---Get Marks
#Finds and returns one marks from database based on player ID

#Operation: Find one
#Collection: marks

def get_mark(mark, mongo):
    filter = {}
    options = {}
    filter['_id'] = mark['_id']
    #del mark['_id']
    try:
        result = mongo.connection.TMDB.marks.find_one(filter)
        return result
    except:     
        print("Exception in get_mark:" + str(filter))
        return False