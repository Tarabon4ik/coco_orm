from typing import Dict
import json
import os
from urllib.parse import urlparse
from urllib.request import urlretrieve

def write_json_file(data, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def read_json_file(filepath: str) -> Dict:
    with open(filepath) as f:
        json_data = json.load(f)
    return json_data


def is_url(value: str) -> bool:
    try:
        result = urlparse(value)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_file_exists(filepath: str):
    return os.path.isfile(filepath)
    
def download(url: str) -> Dict:
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp.json")
    urlretrieve(url, filepath) # download file from a given url
    data = read_json_file(filepath) # read json file as dict
    os.remove(filepath) # remove file from filesystem
    return data
    