"""
Rename files in a folder in order to 000.ogg to 999.ogg
Usage: python rename_files.py [folder]
"""

import os
import sys

FILE_EXT = ".ogg"


def rename_files(folder):
    if not os.path.exists(folder):
        print("Folder '%s' doesn't exist" % folder)
        return
    print("Renaming '*%s' files in '%s'..." % (FILE_EXT, folder))
    files = sorted(os.listdir(folder))
    count = 0
    for i, file in enumerate(files):
        if file.endswith(FILE_EXT):
            name, extension = os.path.splitext(file)
            src = os.path.join(folder, file)
            dst = os.path.join(folder, "%03d%s" % (i, extension))
            os.rename(src, dst)
            count += 1
    print("Done. %d renamed." % count)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
    else:
        rename_files(sys.argv[1])
