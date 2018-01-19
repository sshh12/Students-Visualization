
# coding: utf-8

## Imports

from db import DB

from sklearn.manifold import TSNE
import numpy as np

import hashlib
import random

from cyranchdb import cyranch_db

## Categories

class_types = { # Keywords used to determine class topic
    "socialstudies": ["wd culture", "hist", "gov", "macro eco", "street law", "human geog", "geog", "wd area", "economics"],
    "engineering":   [" arch", "manufac", " manfc", "princ flo des", "auto tech", "pr soln", "arch ", "interior design"],
    "art":           ["floral", " chr", " orch", "art", "band", "animation", "theater", "bnd ", "orchest", "aud vid", "chrl ", "music", "choir", "a/v", "av pro", "voc ens", "symph", "th. pro", " strings"],
    "english":       ["journl ", "journal", "eng ", "creative write", "english", "debate"],
    "science":       ["forensics", "med", "astronomy", "chemsitry", "phys ", "chemistry", "phy/chem", "web tech", "tch sys", "livestock", "electr", "vet med", "wldlif fish eco", "prof comm", "sci", "robot", "physics", "antmy", "physlgy", "biology", "sociology", "animal", "psychology", "chem ", "bio ", "medical", "prin ag fd nt r", "food tech", "com prog"],
    "math":          ["geom", "cal-", "bank financ", "calc", "geometry", "pre cal", "algebra", "statistics", "alg ", "accounting"],
    "language":      ["sign lang", "span i", "spanish", "french", "latin", "german"],
    "sports":        ["ath ", "athletics", "phys ed", "athlet", "cheerleading", "dance", "sports"],
    "other":         [" media", "cosmetology", "info mgmt", "sec invest", "prin of human", " esl", "bim ", "life nutr well", "ipc ics", "car port", "180", "rotc", "spt ent mk", "stu asst", "child ", "intro to cos", "rest mgmt", "rdi 180", "ed trng", " bus", "bus ", " mgt", "pace", "money", "p a l i", "health", "act/sat", "fash des", "child devlp", "fnd pers fit", "teen leadership", "interpers std", "inst ed trg", "hum svc"]
}

def get_class_type(name):

    name = name.lower().strip()

    for subject, kwords in class_types.items():
        for word in kwords:
            if word in name:
                return subject

    return "other"

## Collect Data

data = {}

for index, row in cyranch_db.tables.grades.all().iterrows():
    if row.user_id not in data:
        dic = {
            'name':'?',
            'gender':'?',
            'language':'?',
            'gradelevel':'?',

            'grades':{
                'engineering':[],
                'science':[],
                'math':[],
                'english':[],
                'language':[],
                'art':[],
                'sports':[],
                'socialstudies':[],
                'other':[]
            },

            'classes':{
                'engineering':[],
                'science':[],
                'math':[],
                'english':[],
                'language':[],
                'art':[],
                'sports':[],
                'socialstudies':[],
                'other':[]
            }
        }
        data.update({row.user_id: dic})

    if " AVG" in row['name']:
        continue

    ctype = get_class_type(row.subject)
    data[row.user_id]["grades"][ctype].append(row.grade)
    if not row.subject in data[row.user_id]["classes"][ctype]:
        data[row.user_id]["classes"][ctype].append(row.subject)

for index, row in cyranch_db.tables.demo.all().iterrows():

    try:

        data[row.user_id]["name"] = row.name
        data[row.user_id]["gender"] = row.gender
        data[row.user_id]["language"] = row.language
        data[row.user_id]["gradelevel"] = int(row.gradelevel)

    except Exception as e:
        pass

## Analyze

X = []
labels = []

def avg(nums):
    return round(sum(nums) / float(len(nums))) if len(nums) > 0 else 0

def avg_nonzero(nums):
    return avg(list(filter(lambda n : n > 0, nums)))

ids = list(data.keys())
random.shuffle(ids)

for id_ in ids:

    features = [
        avg_nonzero(data[id_]["grades"]["science"]),
        avg_nonzero(data[id_]["grades"]["math"]),
        avg_nonzero(data[id_]["grades"]["english"]),
        avg_nonzero(data[id_]["grades"]["language"]),
        avg_nonzero(data[id_]["grades"]["art"]),
        avg_nonzero(data[id_]["grades"]["sports"]),
        avg_nonzero(data[id_]["grades"]["socialstudies"]),
        avg_nonzero(data[id_]["grades"]["engineering"])
    ]
    X.append(features)

    # Hashing used to for privacy (although bruteforcing easily possible b/c ids are short)
    h = hashlib.sha256()
    h.update(str(id_.replace("s", "")).encode('utf-8'))

    label = [
        h.hexdigest(),
        data[id_]["gender"],
        data[id_]["language"],
        data[id_]["gradelevel"]
    ]

    labels.append(label)

X_array = np.array(X)

alg = TSNE(n_components=3, learning_rate=10, perplexity=35, n_iter=10000)

new_X = alg.fit_transform(X_array)

## Save

with open('data.js', 'w') as f:

    f.write("\n// AUTO GENERATED FILE\n\n")

    f.write("var points = [\n")
    for x in new_X:
        f.write(repr(list(x)) + ",\n")
    f.write("];\n\n")

    f.write("var labels = [\n")
    for l in labels:
        f.write(repr(l) + ",\n")
    f.write("];\n\n")

    f.write("var features = [\n")
    for row in X:
        f.write(repr(row) + ",\n")
    f.write("];\n\n")
