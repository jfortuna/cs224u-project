import os
import json
from pprint import pprint

#just testing with one transcript to see how the data should be stored
base_path = '../../data/house_hearing_transcripts/'
with open(base_path + 'house_hearing_transcript0.json') as f:
    data = json.load(f)
    pprint(data)
