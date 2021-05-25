from .common import USR_DATA_DIR, DATA_DIR, FIRM_DIR

import lxml.etree as ET
from os.path import os

resource_paths = {
    'user' : USR_DATA_DIR,
    'data' : DATA_DIR,
    'img'   : DATA_DIR,
    'firm'   : FIRM_DIR,
    }
'''Search paths for resource'''

def getRessourcePath(rname):
    try:
        prefix, fname = rname.split(':',1)
        return os.path.join( resource_paths[prefix], fname  )
    except ValueError:
        return rname
    
def getRessourceDir(rtype):
    return resource_paths[rtype]

def ressourceExists(rname):
    return os.path.exists(getRessourcePath(rname))


class PrefixResolver(ET.Resolver):
    def __init__(self, prefix_dict={}):
        self.prefix_dict = prefix_dict  
        
    def resolve(self, url, pubid, context):
        for prefix, replace_path in self.prefix_dict.items():
            if prefix[-1] == ':':
                prefix [:-1]
            if url.startswith(prefix):
                path = os.path.join(replace_path, url[len(self.prefix):])
                return self.resolve_filename(os.path.join(replace_path, path),context)