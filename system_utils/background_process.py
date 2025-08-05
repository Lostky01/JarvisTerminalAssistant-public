import psutil


def get_top_processes(n=5):
    processes = sorted(
        psutil.process_iter(['pid', 'name', 'memory_percent']),
        key=lambda p: p.info['memory_percent'],
        reverse=True
    )
    top = processes[:n]
    lines = [
        f"{p.info['name']} (PID {p.info['pid']}): {p.info['memory_percent']:.2f}% memory"
        for p in top if p.info['name']
    ]
    return "Top memory-hogging processes:\n" + "\n".join(lines)