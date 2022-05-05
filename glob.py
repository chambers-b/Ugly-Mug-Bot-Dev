import os
#Holds constants from config.json
al = {}

faction_list = []
player_list = {} #self.stored_mark = {}
pending_messages = []
sent_messages = []
api_fails = {}
development_mode = ""

if str(os.getenv("REPL_SLUG"))[-3:] == "Dev":
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~~~ Dev Mode ~~~~~~~~~~~~~~~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    development_mode = True
else:
    development_mode = False

# Descriptions of Config parameters
#   Toggles Logging for specific things
#   "debug": false,
#   "travel": false,
#   "mugs": true,
#   "state": false,
#   "messages": true,
#   Send logs to file? Errors are always sent
#   "file_logging": false,
#   Channels to post to
#   "ch_admin": [960573477977460767],
#   "ch_travel": [960572967467749407],
#   "ch_bazaar": [960573756902899782],
#   "ch_mugs": [966758597730136165],
#   Friendly factions
#   "monarch_factions": [],
#   Admins accounts (used for adding api keys)
#   "admins": ["226030188733923328"],
#   Minimum mug amount for buymugs
#   "min_mug_amount": 1000000
#   Minimum amount to show flight
#   "min_on_hand": 10000000