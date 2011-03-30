import sys

try:
    import json
except ImportError:
    import simplejson as json

sys.path.insert(0, 'lib/beaker')
sys.path.insert(0, 'lib/bottle')
sys.path.insert(0, 'lib/gaema')
