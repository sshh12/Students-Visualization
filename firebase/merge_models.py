from collections import defaultdict
import json
import pickle

def make_user():
    return {'grades': []}
users = defaultdict(make_user)

with open('export_transcripts', 'r') as f:
   for line in f.readlines():
       data = json.loads(line)
       sid = data['__key__']['path'].split('", "')[1]
       data['gpa_lastupdated'] = data['lastupdated']
       data['sid'] = sid
       del data['__key__']
       del data['__error__']
       del data['__has_error__']
       del data['lastupdated']
       users[sid].update(data)

with open('export_profiles', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        sid = data['__key__']['path'].split('", "')[1]
        data['demo_lastupdated'] = data['lastupdated']
        data['sid'] = sid
        del data['__key__']
        del data['__error__']
        del data['__has_error__']
        del data['lastupdated']
        users[sid].update(data)

with open('export_grades', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        data = json.loads(line)
        sid = data['__key__']['path'].split('", "')[1]
        del data['__key__']
        del data['__error__']
        del data['__has_error__']
        users[sid]['sid'] = sid
        users[sid]['grades'].append(data)
        break

print('Loaded:', len(users))
with open('export_merged', 'wb') as f:
    pickle.dump(dict(users), f)