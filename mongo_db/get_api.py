#--Get API
#Returns an API from the api server array False result means out of keys

#Operation: Find and Remove (Pop)
#Collection: api_server

import txt_log

def get_api(mongo):
    filter = {}
    options = {}
    mongo.api_call_count += 1
    filter['_id'] = "api_array"
    #options = {'array_list.$': 1}
    update = {"$pop": {"api_list": -1}}
    result = mongo.connection.TMDB.api_server.find_one_and_update(filter, update, )
    #print("API: " + str(result['api_list'][0]))
    if 'api_list' in result.keys() and len(result['api_list']) > 0:
        return result['api_list'][0]
    else:      
        
        txt_log.console("Ran out of API keys. Probably", 'error')
        txt_log.console(str(result), 'error')
    return False