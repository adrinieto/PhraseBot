"""
Crea el json de descripción del dataset
"""
import json
import os
from collections import OrderedDict

DESCRIPTION_FILE = "dataset_template.json"
AUDIO_FOLDER = "data/raw"

files = sorted(os.listdir(AUDIO_FOLDER))

description_template = {
    "path": AUDIO_FOLDER,
    "data": OrderedDict()
}
for file in files:
    if not os.path.isfile(file):
        continue
    description_template["data"][file] = {
        "title": "",
        "keywords": ""
    }
with open(DESCRIPTION_FILE, "w") as fp:
    json.dump(description_template, fp, indent=2)
