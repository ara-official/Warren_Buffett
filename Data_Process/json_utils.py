import json
from collections import OrderedDict


def json_read(json_file_name, key):
    print("json file " + json_file_name)
    json_file_name="../json/"+json_file_name
    with open(json_file_name, "r") as json_file:
        json_data = json.load(json_file)
    return json_data[key]

def json_write(json_file_name, key, value=""):
    print("json file " + os.path.dirname( os.path.abspath( __file__ ) )+json_file_name)
    json_file_name="War/json/"+json_file_name
    file_data = dict()
    file_data[key] = value
    json.dumps(file_data, ensure_ascii=False, indent="\t")
    with open(json_file_name, 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
