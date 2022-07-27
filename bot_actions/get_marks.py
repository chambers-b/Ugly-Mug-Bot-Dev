from ext import *  #Import external package set

import torn_api
import mongo_db
import txt_log
import message_builder
import glob


from bot_actions.message_channel import message_channel
from bot_actions.compare_states import compare_states

#X---Get Marks (targets) "The Brain"
#The first really complicated function pulls api via faction calls and looks for changes from the database, needs to track the timing of changes, eventually pull bazaar value and estimate a landing time.

def get_marks(faction_list, mongo, client):
    txt_log.console("bot_actions.get_marks", "debug")
    #message_channel("Testing", [960573477977460767], client)
    user_count = 0
    ms = datetime.datetime.now()
    start_time = time.mktime(ms.timetuple())
    for faction in faction_list:
        if faction == 0:
            continue
        faction_obj = torn_api.get_members(faction, mongo)
        if faction_obj is False:
            txt_log.console("Escaping get_marks", "error")
            return False
        members = faction_obj['members']
        #print("Faction: " + str(faction) + " " + faction_obj['name'])
        #multi-thread this shit!
        ms = datetime.datetime.now()
        #print(time.mktime(ms.timetuple()))
        for member_id in members:
            user_count += 1
            member_obj = members[member_id]
            #print(member_id)
            mark = {}
            mark['_id'] = member_id
            mark['name'] = member_obj['name']
            mark['last_update'] = time.mktime(ms.timetuple())
            mark['faction'] = faction
            mark['status'] = member_obj['last_action']['status']
            mark['description'] = member_obj['status']['description']
            mark['state'] = member_obj['status']['state']
            if member_id not in glob.player_list.keys():
                #print("Retrieving " + str(member_id))
                glob.player_list[member_id] = mongo_db.get_mark(mark, mongo)
                
              
            if member_id not in glob.player_list.keys() or glob.player_list[member_id] == None: 
                try:
                    print(str(member_obj['name']) + " [" + str(member_id) + "]")
                    print(glob.player_list[member_id])
                except:
                    pass
                print("New: " + str(member_obj['name']) + " [" + str(member_id) + "]")
                mongo_db.update_mark(mark, mongo) 
                glob.player_list[member_id] = mark
            else:
                compare_result = compare_states(glob.player_list[member_id], mark, mongo, client)
                if compare_result is False:
                    txt_log.log("bot_actions.compare_states returned False in get_marks")
                
                    return False
                glob.player_list[member_id] =  compare_result
        mongo_db.update_timestamp(int(faction), mongo)
              
                
            
    ms = datetime.datetime.now()
    #print("Duration: " + str(time.mktime(ms.timetuple()) - start_time) + " seconds for " + str(len(faction_list)) + " factions with " + str(user_count) + " members.")
    mongo.user_count += user_count
    mongo.faction_count += len(faction_list)
    
    
