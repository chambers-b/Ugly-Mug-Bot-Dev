from datetime import datetime
import glob

#NEW - txt_log instead of passing funny error messages
def log(text):
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    file_object = open('log.txt', 'a')
    file_object.write("\n" + current_time + " " + str(text))
    file_object.close()

#config.json
#Read once per minute on database connection open
# {
#   "debug": True,
#   "travel": True,
#   "state": True,
#   "messages": True,
#   "file_logging": True,
# }
def console(text, log_type):
    if glob.al['debug'] is True and log_type == "debug":
        print(str(text))
        if  glob.al['file_logging'] is True: log(str(text))
    if glob.al['travel'] is True and log_type == "travel":
        print(str(text))
        if  glob.al['file_logging'] is True: log(str(text))
    if glob.al['state'] is True and log_type == "state":
        print(str(text))
        if  glob.al['file_logging'] is True: log(str(text))
    if glob.al['messages'] is True and log_type == "messages":
        print(str(text))  
        if  glob.al['file_logging'] is True: log(str(text))
    if glob.al['mugs'] is True and log_type == "mugs":
        print(str(text))  
        if  glob.al['file_logging'] is True: log(str(text))
    if log_type == "error":
        print(str(text))  
        if  glob.al['file_logging'] is True: log(str(text))
    if log_type not in ["debug", "travel", "state", "messages", "error", "mugs"]:
        #Always printed because this is an error
        print("Unrecognized error type: " + str(log_type))
        print(str(text)) 

          
    
