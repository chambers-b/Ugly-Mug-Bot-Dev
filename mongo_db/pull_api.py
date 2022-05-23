#--Pull Api
#Removes this key from the API server array

#Operation: Pull (Remove a specific value)
#Collection: api_server

import mongo_connector

def pull_api(api):
    filter = {}
    options = {}
    filter['_id'] = "api_array"
    #options = {'array_list.$': 1}
    update = {"$pull": {"api_list": api}}
    try:
        mongo = mongo_connector.SilentConnection()
        with mongo:
            result = mongo.connection.TMDB.api_server.update_one(filter, update)
            
        return True
    except:        
        return False  