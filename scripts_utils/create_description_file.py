"""
Create the template of the description file for the dataset
Usage: python create_description_file.py [folder]
"""
import json
import os
from collections import OrderedDict

import sys

DESCRIPTION_FILE = "dataset_template.json"
FILE_EXT = ".txt"


def create_description_file(folder):
    if not os.path.exists(folder):
        print("Folder '%s' doesn't exist" % folder)
        return
    files = sorted([file for file in os.listdir(folder) if file.endswith(FILE_EXT)])
    if len(files) == 0:
        print("Folder '%s' doesn't have any '%s' files" % (folder, FILE_EXT))
        return
    output_file = os.path.join(folder, DESCRIPTION_FILE)
    if os.path.exists(output_file):
        print("Description file '%s' already exists" % output_file)
        return
    dataset_description = OrderedDict([
        ("path", folder),
        ("mention_words", []),
        ("data", OrderedDict())
    ])
    count = 0
    for file in files:
        dataset_description["data"][file] = {
            "title": "",
            "keywords": ""
        }
        count += 1
    print(dataset_description)
    with open(output_file, "w") as fp:
        json.dump(dataset_description, fp, indent=2)
    print("Created description file in '%s' with %d files." % (folder, count))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
    else:
        create_description_file(sys.argv[1])
