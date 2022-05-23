# #--Add Message Log  

#Operation: Update
#Collection: active_alerts

import mongo_connector

def add_message(mark, channel_type, message_list, mongo):
    
    options = {
      'player_id': mark['_id'], 
      'name': mark['name'],
      'faction': mark['faction'],
      'type': channel_type, 
      'message_list':message_list,     
      }
    if channel_type == 'travel':
        options['landing_time'] = mark['landing_time']
    try:
        mongo = SilentConnection()
        with mongo:
            result = mongo.connection.TMDB.active_alerts.insert_one(options)
            #print(result.upserted_id)
        return True
    except:
      return "Exception: mongo_db.add_message"

#buy mug mark:{'_id': '2034640', 'name': 'lightnemesis', 'last_update': 1651854592.0, 'faction': 27223, 'status': 'Offline', 'description': 'Okay', 'state': 'Okay'} 
#travel mark:{'_id': '2731392', 'name': 'Andeafdod', 'last_update': 1651856448.0, 'faction': 25025, 'status': 'Online', 'description': 'Returning to Torn from Switzerland', 'state': 'Traveling', 'landing_time': 1651863915.0, 'depart_cash': 3100750, 'landing_cash': 2465000}