#--Add Api      
#Adds API to api_keys table as public
import mongo_connector
#Operation: Update
#Collection: api_keys

def add_api(torn_id, api, discord_id, rate):
    filter = {}
    options = {}
  
    try:
        filter['_id'] = torn_id
        #options['_id'] = torn_id
        options['api'] = api
        options['discord_id'] = discord_id
        options['type'] = 'public'
        options['rate'] = rate
        mongo = mongo_connector.SilentConnection()
        with mongo:
            result = mongo.connection.TMDB.api_keys.update_one(filter, {"$set": options}, upsert=True)
            #print(result.upserted_id)
        return "API successfully registered allowing " + str(rate) + " calls per minute."
    except:
      return "Exception: mongo_db.add_api"