import datetime
now = datetime.datetime.now()
global_hour = now.hour
if global_hour < 12:
    global_greeting = "Good morning"
elif global_hour < 18:
    global_greeting = "Good afternoon"
else:
    global_greeting = "Good night"

    print("{}!".format(global_greeting))