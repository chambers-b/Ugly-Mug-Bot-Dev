#Removes an api from the key table

#Operation: Delete
#Collection: api_keys

import mongo_connector

def rm_api(filter):
    
    try:
        mongo = mongo_connector.SilentConnection()
        with mongo:
            #print(filter)
            result = mongo.connection.TMDB.api_keys.delete_many(filter)
            #print(result)
            if result.acknowledged:
                if result.deleted_count > 0:
                    return "User data deleted. Please also change your API if you have a security concern. https://www.torn.com/preferences.php#tab=api"
                else:
                    return "No data was found nothing was deleted."
    except:
        return "Exception: mongo_db.rm_api (unknown response from database)"