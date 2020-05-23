import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

def json_read(json_file_name, key):
    reletive_path=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    json_file_name=str(reletive_path)+'\\json\\'+json_file_name
    # print("[read] json file " + json_file_name)
    
    with open(json_file_name, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return json_data[key]

def json_write(json_file_name, key, value=""):
    
    reletive_path=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    json_file_name=str(reletive_path)+'\\json\\'+json_file_name
    # print("[write] json file " + json_file_name)
    
    file_data = dict()
    file_data[key] = value
    json.dumps(file_data, ensure_ascii=False, indent="\t")
    with open(json_file_name, 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
