#!/usr/bin/python

import sys

from wsgiref.handlers import CGIHandler
from chords import app

path = "/home/kcwangluckychordmanager"

if path not in sys.path:
    sys.path.insert(0, path)
    # sys.path.insert(0, "~/.local/lib/python2.7/site-packages")

CGIHandler().run(app)
