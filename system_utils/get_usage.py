import psutil

def get_cpu_usage():
    return f"Cpu usage is at {psutil.cpu_percent()}%."

def get_ram_usage():
    mem = psutil.virtual_memory()
    return f"RAM usage: {mem.percent}% used, {round(mem.used / (1024**3), 2)}GB of {round(mem.total / (1024**3), 2)}GB."

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return f"Disk usage: {disk.percent}% used, {round(disk.used / (1024**3), 2)}GB of {round(disk.total / (1024**3), 2)}GB."