import pymongo
import os
import time
import datetime
import json

class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self):
        ms = datetime.datetime.now()
        self.start_time = time.mktime(ms.timetuple())
        self.connection = None
        self.api_call_count = 0
        self.faction_count = 0
        self.user_count = 0
        self.excluded_categories = ["Melee", "Secondary", "Primary", "Defensive", "Clothing", "Other", "Collectible"]
        print("Class Connection Initiated")
    def __enter__(self):
        self.connection = pymongo.MongoClient(os.getenv('Mongo_URL'), connect=True)
        print("Class Connection Entered")
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print("~~~Connection Statistics~~~")
        ms = datetime.datetime.now()
        print(" Duration: " + str(time.mktime(ms.timetuple())-self.start_time) +" seconds")
        print("API Calls: " + str(self.api_call_count))
        print(" Factions: " + str(self.faction_count))
        print("    Users: " + str(self.user_count))
        print("~~~Class Connection Closed~~~")