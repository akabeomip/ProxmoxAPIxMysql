import os
import json

def jsonSave(filename, info, now):
    if not os.path.exists(f"U:\MWG\\api\\{now}"):
        os.mkdir(f"U:\MWG\\api\\{now}")
    with open(f"U:\MWG\\api\\{now}\\{filename}.json", 'a') as f:
        json.dump(info, f)
        f.write(', ')