import subprocess
from datetime import datetime
def time():
    now = datetime.utcnow()
    
    current_time = now.strftime("%H:%M")

    subprocess.call(["espeak", "The current time is" + current_time])
    print("The current time is:", current_time)
