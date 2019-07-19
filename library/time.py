from datetime import datetime
def time():
    now = datetime.now()
    
    current_time = now.strftime("%H:%M")

    print("The current time is:", current_time)
