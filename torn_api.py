#All api code goes here
#Need to add error checking
import requests
import json
import os
import threading

import txt_log
import mongo_db
import glob


#Example
#https://api.torn.com/user/?selections=personalstats&stat=defendswon,defendslost&timestamp=1650556811&key=
#personalstats&stat=useractivity&timestamp=-5days

#X---Get Faction List
#Uses territory api call to get list of factions
#Need to build in a size cutoff or max number of factions due to not having enough API keys currently. Can be a constant defined above or something passed from main.
#[123456, 345566, 44555, 24444]
#Returns list [Success t/f, result list]
def get_faction_list(mongo):
    try:
        api = mongo_db.get_api(mongo)
        try:
            mongo.api_call_count += 1
        except:
            pass
        if api is False:
            txt_log.log("mongo_db.get_api returned False in get_faction_list")
            return False
        r = requests.get("https://api.torn.com/torn/?selections=territory&key=" + str(api))
        faction_list = {}
        territories = r.json()['territory']
        for territory in territories:
            faction_list[territories[territory]['faction']] = True
        keys = list(faction_list.keys())
        keys.sort()
        print("Returned " + str(len(keys)) + " factons.")
        return [True, keys]
    except:
        api_error(r.json()['error'], api)
        return [False, r.json()['error']['error']]

#---Get Members
#Uses faction api call to get list of mambers and status
#Strip out extra faction info so that the object is a 
#dictionary of mark_id's with nested attributes
def get_members(faction, mongo):
    for x in range(10):
        api = mongo_db.get_api(mongo)
        if api is False:
            txt_log.log("mongo_db.get_api returned False in get_members")
            return False
        r = requests.get("https://api.torn.com/faction/" + str(faction) + "?selections=&key=" + api)
        try:
            api_error(r.json()['error'], api)
        except:
            pass
        
        return r.json()
    return False

#Checks if API keys user is verified and if they are the one submitting it.
def check_if_verified(message, api):
    try:
        r = requests.get("https://api.torn.com/user/?selections=discord&key=" + api)
        discord_id = r.json()['discord']['discordID']
        torn_id = r.json()['discord']['userID']
        print(discord_id)
        print(message.author.id)
        #--Admin Override allowing entry of API 
        if str(message.author.id) in glob.al['admins']:
            return [True, torn_id, discord_id]
        #--
        if str(message.author.id) == str(discord_id):
            return [True, torn_id, discord_id]
        elif discord_id == "":
            return [False, "User is not verified."]
        else:
            return [False, "Please use your own API."]
        pass
    except:
        return [False, r.json()['error']['error']]

      
#--API Error Handler
def api_error(error_obj, api):
    print("Error received: " + str(error_obj['error'] + " " + api))
    txt_log.log("Torn API error: " + str(error_obj['error'] + " " + api))
    print("Torn API error: " + str(error_obj['error'] + " " + api))
    #print(str(api))
    error_code = error_obj['code']
    if error_code == 5:
        #Too many requests from api_error
        #Drop this API from the database array
        mongo_db.pull_api(api)
        return True
    elif error_code in [2, 10, 13]:
        #2 - Private key is wrong/incorrect format.
        #10 - Key owner in Fed
        #13 - Key owner inactive
        #Did user delete key? User fedded? User inactive?
        #Remove key from database
        filter = {}
        filter['api'] = api
        if api in api_fails.keys():
            api_fails[api] += 1
        else:
            api_fails[api] = 1
        mongo_db.pull_api(api)
        if api_fails[api] > 9:
            mongo_db.rm_api(filter)
        return True
    elif error_code == 8:
        #IP Blocked you fool!
        print("YOU ARE IP BLOCKED STOP EVERYTHING")
        print("Exiting program.")
        os._exit(0)
    else:
        print("Unknown Cause, not handled." + str(error_code))
        return False
#--Get Bazaar
#Pulls bazaar data and calculates some supplementary data which is added to the object
#Use the error checking here as template
def get_bazaar(torn_id, mongo):
    #print(faction)
    for x in range(10):
        api = mongo_db.get_api(mongo)
        #Test for False
        if api is False:
            txt_log.log("mongo_db.get_api returned False in get_bazaar")
            return False
        
        r = requests.get("https://api.torn.com/user/" + str(torn_id) + "?selections=bazaar&key=" + api)
        try:
            total_value = 0
            buy_mug_value = 0
            total_potential_mug_value = 0
            bazaar_obj = r.json()
            for item in bazaar_obj['bazaar']:
                total_value += item['quantity'] * item ['price']
                if item['price'] > 1 and item['market_price'] > 1000 and item['type'] not in glob.al['excluded_categories'] and item['name'] not in glob.al['excluded_items']:
                    potential_mug_value = (item['market_price'] - 0.925*item['price'])*item['quantity']
                    if potential_mug_value > 0:
                        total_potential_mug_value += potential_mug_value
                        buy_mug_value += item['quantity'] * item ['price']
            #print("Total Value: " + str(total_value))
            bazaar_obj['bazaar_value'] = total_value
            bazaar_obj['buy_mug_value'] = buy_mug_value
            bazaar_obj['potential_mug_value'] = total_potential_mug_value
            return bazaar_obj
        except:
            api_error(r.json()['error'], api)
    return False

#NEW
def get_profile(torn_id, mongo=False, api=""):
    #print(faction)
    for x in range(10):
        if mongo != False:
            api = mongo_db.get_api(mongo, True)
        #Test for False
        if api is False:
            txt_log.log("mongo_db.get_profile returned False in get_bazaar")
            return False
        
        r = requests.get("https://api.torn.com/user/" + str(torn_id) + "?selections=profile&key=" + api)
        try:
            player_obj = r.json()
            player_obj['_id'] = player_obj['player_id']
            return player_obj
        except:
            api_error(r.json()['error'], api)
    return False


def get_stats(torn_id, mongo):
    #print(faction)
    for x in range(10):
        api = mongo_db.get_api(mongo)
        #Test for False
        if api is False:
            txt_log.log("mongo_db.get_stats returned False in get_bazaar")
            return False
        
        r = requests.get("https://api.torn.com/user/" + str(torn_id) + "?selections=personalstats&key=" + api)
        player_obj = r.json()
        if "personalstats" in player_obj.keys():
            player_obj['_id'] = torn_id
            return player_obj
        else:
            api_error(r.json()['error'], api)
    return False

#NEW
#API TEMPLATE WITH DESCRIPTORS
def get_TEMPLATE(torn_id, mongo):
    #If it fails try again with a different key
    for x in range(10):
        api = mongo_db.get_api(mongo)
        #If False then the database is out of keys and this cycle needs to terminate without further loops
        if api is False:
            txt_log.log("mongo_db.get_stats returned False in get_bazaar")
            return False
        #Try API Call
        r = requests.get("https://api.torn.com/user/" + str(torn_id) + "?selections=personalstats&key=" + api)
        player_obj = r.json()
        #If else or try/except to check the response for what we need 
        #try:
        if "personalstats" in player_obj.keys():
            player_obj['_id'] = torn_id
            return player_obj

        #If the response is bad pass the api to the error module (which logs it)
        #except:
        else:
            api_error(r.json()['error'], api)
    #If it fails 10 times something is wrong so terminate this cycle
    return False