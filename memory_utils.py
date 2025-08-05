# memory_utils.py

import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"conversations": []}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def add_to_memory(user_input, jarvis_response):
    memory = load_memory()
    memory["conversations"].append({
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "jarvis": jarvis_response
    })
    # Cap memory to last 100 interactions
    memory["conversations"] = memory["conversations"][-100:]
    save_memory(memory)

def get_last_n_conversations(n=5):
    memory = load_memory()
    return memory["conversations"][-n:]
