import datetime
now = datetime.datetime.now()
def greeting(hour):
  if hour < 12:
    return  "Good morning"
  elif hour < 18:
    return  "Good afternoon"
  else:
    return  "Good night"