#---Get Marks
#Finds and returns one marks from database based on player ID

#Operation: Find
#Collection: marks

import mongo_connector

def get_mark_collection():
    filter = {}
    options = {}
    player_list = {}
    print("~~~ Retrieving Player List (M)")
    #del mark['_id']
#try:
    mongo = mongo_connector.SilentConnection()
    with mongo:
        result = mongo.connection.TMDB.marks.find(filter)
        for player in result:
            player_list[player['_id']] = player
    return player_list
#except:     
    print("Exception in get_mark_collection:" + str(filter))
    return False  