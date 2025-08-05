import os
import subprocess

def search_file_system(keyword, search_dir="C:/", max_depth=5):
    matches = []

    def recursive_search(current_dir, depth):
        if depth > max_depth:
            return
        try:
            for root, dirs, files in os.walk(current_dir):
                for name in files + dirs:
                    if keyword.lower() in name.lower():
                        full_path = os.path.join(root, name)
                        matches.append(full_path)
                break 
            for d in dirs:
                recursive_search(os.path.join(current_dir, d), depth + 1)
        except Exception:
            pass

    recursive_search(search_dir, 0)
    return matches

def open_in_explorer(path):
    if os.path.exists(path):
        explorer_path = os.path.dirname(path) if os.path.isfile(path) else path
        subprocess.run(f'explorer "{explorer_path}"')
        return f"Opened {explorer_path}"
    return "Path does not exist."
