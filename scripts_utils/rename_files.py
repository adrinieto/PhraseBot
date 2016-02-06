"""
Renombra los ficheros de un directorio por orden desde 000.ext en orden ascendente
"""

import os

AUDIO_FOLDER = "data/raw"

files = sorted(os.listdir(AUDIO_FOLDER))
for i, file in enumerate(files):
    name, extension = os.path.splitext(file)
    src = os.path.join(AUDIO_FOLDER, file)
    dst = os.path.join(AUDIO_FOLDER, "%03d%s" % (i, extension))
    os.rename(src, dst)