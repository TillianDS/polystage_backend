from datetime import datetime

def getDate(date_str):
    date = datetime.strptime(date_str, '%d-%m-%Y').date()
    return date    

def getTime(time_str):
    time = datetime.strptime(time_str, '%H:%M').time()
    return time