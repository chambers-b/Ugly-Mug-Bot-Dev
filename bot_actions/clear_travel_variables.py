#Clears certain variables when player is in Torn
def clear_travel_variables(new, change):
    if 'depart_time' in new.keys():
        del new['depart_time']
        change = True
    if 'travel_time' in new.keys():
        del new['travel_time']
        change = True
    if 'landing_time' in new.keys():
        del new['landing_time']
        change = True
    if 'depart_cash' in new.keys():
        del new['depart_cash']
        change = True
    if 'landing_cash' in new.keys():
        del new['landing_cash']
        change = True  
    return new, change