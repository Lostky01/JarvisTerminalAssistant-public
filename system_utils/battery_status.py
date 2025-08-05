import psutil


def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        plugged = "charging" if battery.power_plugged else "not charging"
        return f"Battery is at {battery.percent}% and is currently {plugged}."
    else:
        return "I couldn't find a battery on this device."

