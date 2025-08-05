import time
import psutil



def get_uptime():
    seconds = time.time() - psutil.boot_time()
    minutes = int(seconds / 60 % 60)
    hours = int(seconds / 3600 % 24)
    days = int(seconds / 86400)
    return f"System uptime is {days} days, {hours} hours, and {minutes} minutes."

