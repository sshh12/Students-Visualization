"""
Merge data from 3 export files into a friendly
pickle bin file.
"""
from collections import defaultdict
import json
import pickle
import dateutil.parser
from datetime import datetime


NOW = datetime.now()
NEXT_JULY = NOW.replace(month=7, tzinfo=None)
if NOW.month > 6:
    NEXT_JULY = NEXT_JULY.replace(year=NOW.year + 1)

def make_user():
    return {'grades': []}

users = defaultdict(make_user)

with open('export_transcripts', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        sid = data['__key__']['path'].split('", "')[1]
        data['gpa_lastupdated'] = dateutil.parser.parse(data['lastupdated'])
        data['sid'] = sid
        data['rank'] = int(data['rank'])
        data['classsize'] = int(data['classsize'])
        data['gpa'] = float(data['gpa'])
        data['autoadmit'] = 'yes' if ((data['rank'] / data['classsize']) < 0.06) else 'no'
        del data['__key__']
        del data['__error__']
        del data['__has_error__']
        del data['lastupdated']
        users[sid].update(data)

with open('export_profiles', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        sid = data['__key__']['path'].split('", "')[1]
        data['demo_lastupdated'] = dateutil.parser.parse(data['lastupdated'])
        data['sid'] = sid
        data['gradelevel'] = int(data['gradelevel'])
        # adjust for stale grade level data
        data_age = (NEXT_JULY - data['demo_lastupdated'].replace(tzinfo=None)).days
        data['adjgradelevel'] = data['gradelevel'] + data_age // 365
        del data['__key__']
        del data['__error__']
        del data['__has_error__']
        del data['lastupdated']
        users[sid].update(data)

with open('export_grades', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        data = json.loads(line)
        sid = data['__key__']['path'].split('", "')[1]
        if 'lastupdated' in data:
            data['lastupdated'] = dateutil.parser.parse(data['lastupdated'])
        del data['__key__']
        del data['__error__']
        del data['__has_error__']
        users[sid]['sid'] = sid
        users[sid]['grades'].append(data)

print('Loaded:', len(users))
with open('export_merged', 'wb') as f:
    pickle.dump(dict(users), f)