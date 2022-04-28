#Things that touch the database (pymongo)
#If it uses pymongo it goes here

import pymongo
import os
import dns
import json

import txt_log
import glob

##### DO NOT INSTALL "BSON" ######
# To fix, uninstall BSON from left package manager
# Delete poetry and tomal lock files
# pip uninstall pymongo
# pip3 install pymongo



#Try to keep connections open for multiple calls, rate is measured per connections 
#eg. with mongo: do more transactions
#DNU compatibility
class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = pymongo.MongoClient(os.getenv('Mongo_URL'))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

#API Table
#The database has a scheduled trigger that creates a large array list (API server array) every minute, as they are called they "pop" and are regenerated the next minute.
      
#--Get API
#Returns an API from the api server array False result means out of keys
def get_api(mongo):
    filter = {}
    options = {}
    mongo.api_call_count += 1
    filter['_id'] = "api_array"
    #options = {'array_list.$': 1}
    update = {"$pop": {"api_list": -1}}
    try:
        result = mongo.connection.TMDB.api_server.find_one_and_update(filter, update, )
        #print("API: " + str(result['api_list'][0]))
      
        return result['api_list'][0]
    except:        
        print("Out of API Keys")
        txt_log.log("Ran out of API keys.")
        return False

#--Pull Api
#Removes this key from the API server array
def pull_api(api):
    filter = {}
    options = {}
    filter['_id'] = "api_array"
    #options = {'array_list.$': 1}
    update = {"$pull": {"api_list": api}}
    try:
        mongo = MongoDBConnection()
        with mongo:
            result = mongo.connection.TMDB.api_server.update_one(filter, update)
            
        return True
    except:        
        return False  


#--Add Api      
#Adds API to api_keys table as public
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
        mongo = MongoDBConnection()
        with mongo:
            result = mongo.connection.TMDB.api_keys.update_one(filter, {"$set": options}, upsert=True)
            #print(result.upserted_id)
        return "API successfully registered allowing " + str(rate) + " calls per minute."
    except:
      return "Exception: mongo_db.add_api"

def rm_api(filter):
    try:
        mongo = MongoDBConnection()
        with mongo:
            result = mongo.connection.TMDB.api_keys.delete_many(filter)
            
            if result.acknowledged:
                if result.deleted_count > 0:
                    return "User data deleted. Please also change your API if you have a security concern. https://www.torn.com/preferences.php#tab=api"
                else:
                    return "No data was found nothing was deleted."
    except:
        return "Exception: mongo_db.rm_api (unknown response from database)"
      
#---Get Marks
#Finds and returns one marks from database based on player ID
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

#---Update Marks
#Updates one mark based on player ID
def update_mark(mark, mongo):
    filter = {}
    options = {}
    filter['_id'] = mark['_id']
    try:
        result = mongo.connection.TMDB.marks.replace_one(filter, mark,upsert=True)
        return True
    except:
        print("Exception in update_mark:" + str(filter))
        return False




      

###
###Examples from Stockbot below this point!!!!!!!!! 
###
# #Notifications__________________________________
# def add_notif(ctx, args):
#     options = {}
#     try:
#         options['discord_id'] = ctx.author_id
#         options['discord_name'] = ctx.author.name
#     except:
#         options['discord_id'] = ctx.author.id
#         options['discord_name'] = ctx.author.name
#     options.update(args)
#     options['value'] = float(options['value'])
#     try:
#         mongo = MongoDBConnection()
#         with mongo:
#             if mongo.connection.TMDB.notifications.find(options).count() == 0:
#                 mongo.connection.TMDB.notifications.insert_one(options)
#                 return "Added "
#             else:
#                 return "Notification Exists"
#     except:
#         print("Adding Failed")
#         return 'Failed'

# def get_notif(ctx, args):
#     options = args
#     #options.update(args)
    
#     if 'value' in options.keys():
#         try:
#             options['value'] = float(options['value'])
#         except:
#             pass
#     #try:
#     print(options)
#     mongo = MongoDBConnection()
#     output = ""
#     with mongo:
#         if mongo.connection.TMDB.notifications.find(options).count() > 0:
#             for results in mongo.connection.TMDB.notifications.find(options, constants.proj_omissions):
#                 #print(results)
#                 output = functions.table_builder(results, output)
#                 if len(output) > 1800:
#                     output = output + "More results hidden...\n"
#                     break
#             #print(output)
#             return "```\n" + output + "\n```"
#         else:
#             return "No Results"
#     # except:
#     #     print("Database is down!")
#     #     return "Error with database function."

# def add_notif_from_import(args):
#     options = {}
#     options.update(args)
#     options['value'] = float(options['value'])
#     try:
#         mongo = MongoDBConnection()
#         with mongo:
#             if mongo.connection.TMDB.notifications.find(options).count() == 0:
#                 mongo.connection.TMDB.notifications.insert_one(options)
#                 print("Added Sucessfully")
#             else:
#                 print("Notification Exists")
#     except:
#         print("Adding Failed")
#         return 'Failed'
# def update_notif(ctx, args, pause=False):
#     options = args
#     #options.update(args)
#     if 'value' in options.keys():
#         try:
#             options['value'] = float(options['value'])
#         except:
#             pass
#     try:
#         mongo = MongoDBConnection()
#         output = ""
#         with mongo:
#             if mongo.connection.TMDB.notifications.find(options).count() > 0:
#                 if pause == True:
#                     mongo.connection.TMDB.notifications.update_many(options, {"$set":{'pause': True}})
#                 else:
#                     mongo.connection.TMDB.notifications.update_many(options, {"$unset":{'pause': ''}})
#                 for results in mongo.connection.TMDB.notifications.find(options, constants.proj_omissions):   
#                     output = functions.table_builder(results, output)
#                     #print(output)
#                 return "```\n" + output + "\n```"
#             else:
#                 return "No Results"
#     except:
#         print("Database is down!")
#         return "Error with database function."

# def delete_notif(options):
#     # try:
#         mongo = MongoDBConnection()
#         output = ""
#         print(options)
#         with mongo:
#             if mongo.connection.TMDB.notifications.find(options).count() > 0:
#                 for results in mongo.connection.TMDB.notifications.find(options, constants.proj_omissions):
#                     output = functions.table_builder(results, output)
#             mongo.connection.TMDB.notifications.delete_many(options)
#             return "Deleted Records:\n```\n" + output + "\n```"
#     # except:
#     #     print("Database is down!")
#     #     return -2

# def check_notif():
# #Returns all notifications for parsing
#     try:
#         #Returns a list of results
#         mongo = MongoDBConnection()
#         output = []
#         with mongo:
#             if mongo.connection.TMDB.notifications.find({}).count() > 0:
#                 for results in mongo.connection.TMDB.notifications.find({}):
#                     #key = str(results.get('_id'))
#                     output.append(results)
#                     #output.update(results)
#                 print(str(len(output)) + " notifications exist.")
#                 return output
#             else:
#                 print("No Results")
#                 return -1
#     except:
#         print("Database is down during notification grab!")

# def update_by_id(id, updates):
#     # try:
#         #Returns a list of results
#         mongo = MongoDBConnection()
#         with mongo:
#             mongo.connection.TMDB.notifications.update_one({"_id": ObjectId(id)}, {"$set":updates})
#             return 1
# #Queries__________________________________
# def add_query(args):
#     try:
#         mongo = MongoDBConnection()
#         with mongo:
#             mongo.connection.TMDB.queries.insert_one(args)
#         return "Added Sucessfully"
#     except:
#         print("Adding Query Failed")
#         return 'Failed'

# def get_query(msg_id):
#     mongo = MongoDBConnection()
#     with mongo:
#         result = mongo.connection.TMDB.queries.find_one({'msg_id': msg_id})
#         #print("Result: "+ str(result))
#         del result['msg_id']
#         del result['_id']
#     return result

# def check_query(options):
# #Returns all notifications for parsing
#     try:
#         #Returns a list of results
#         mongo = MongoDBConnection()
#         output = []
#         with mongo:
#             if mongo.connection.TMDB.queries.find(options).count() > 0:
#                 for results in mongo.connection.TMDB.queries.find(options):
#                     #key = str(results.get('_id'))
#                     output.append(results)
#                     #output.update(results)
#                 print(str(len(output)) + " queries are cached.")
#                 return output
#             else:
#                 print("No Results")
#                 return output
#     except:

#         print("Database is down during notification grab!")
# # def add_api(ctx, args):
# #     options = {}
# #     options['discord_id'] = ctx.author_id
# #     try:
# #         mongo = MongoDBConnection()
# #         with mongo:
# #             if mongo.connection.TMDB.keys.find(options).count() == 0:
# #                 mongo.connection.TMDB.keys.insert_one(options)
# #                 return "Added Sucessfully"
# #             else:
# #                 return "Notification Exists"
# #     except:
# #         print("Adding Failed")
# #         return 'Failed'

# #DB_Check__________________________________
# def db_check():
#     try:
#         mongo = MongoDBConnection()
#         output = ""
#         with mongo:
#             collection = mongo.connection.TMDB.users
#             serverStatusResult = mongo.connection.TMDB.command("serverStatus")
#             output = "MongoDB is live at: " + str(serverStatusResult['localTime']) + '\n' + "Host: " + str(serverStatusResult['host']) + '\n' + "version: " + str(serverStatusResult['version'])
#             print(serverStatusResult)
#             return output
#     except:
#         print("Database is down!")
#         return "Database is down!"


# #Prices__________________________________
# def get_price(options):
#     print(options)
#     try:
#         mongo = MongoDBConnection()
#         output = ""
#         with mongo:
#             if mongo.connection.TMDB.prices.find(options).count() > 0:
#                 for results in mongo.connection.TMDB.prices.find(options):
#                     return results
#             else:
#                 return "No Results"
#     except:
#         print("Database is down!")
#         return "Error with database function."

# def get_last_price():
#     # try:
#     mongo = MongoDBConnection()
#     output = ""
#     with mongo:
#         for results in mongo.connection.TMDB.prices.find({}).sort('_id', -1).limit(1):
#             return results
#         # else:
#         #     return "No Results"
#     # except:
#     #     print("Database is down!")
#     #     return "Error with database function."


# #Trader____________________________________________
# def create_trader(ctx, args):
#     mongo = MongoDBConnection()
#     with mongo:
#         status = mongo.connection.TMDB.keys.update_one({"_id": ctx.author_id}, {"$set":{'api':args['api'], 'public': args['public']}}, True)
#         print(str(status))

# def get_trader(discord_id):

#     try:
#         mongo = MongoDBConnection()
#         output = ""
#         with mongo:
#             if mongo.connection.TMDB.keys.find({'_id':discord_id}).count() > 0:
#                 for results in mongo.connection.TMDB.keys.find({'_id':discord_id}):
#                     return results
#             else:
#                 return "No Results"
#     except:
#         print("Database is down!")
#         return "Error with database function."

    
# def create_transaction(t, args):
#     mongo = MongoDBConnection()
#     try:
#         with mongo:
#             status = mongo.connection.TMDB.stock_transaction.update_one({"_id": t}, {"$set":args}, True)
#     except:
#         print("Upload of transactions failed.")

# def get_transactions(discord_id):
# #Returns all notifications for parsing
#     #try:
#         #Returns a list of results
#     mongo = MongoDBConnection()
#     output = []
#     with mongo:
#         if mongo.connection.TMDB.stock_transaction.find({'discord_id':discord_id, 'processed':False}).count() > 0:
#             for results in mongo.connection.TMDB.stock_transaction.find({'discord_id':discord_id, 'processed':False}).sort('timestamp', -1):
                
#                 output.append(results)
#                 #output.update(results)
#                 #print(output)
#             return output
#         else:
#             print("No Results")
#             return -1
#     # except:
    #     print("Error in transaction grab!")
