from cyranchdb import cyranch_db
from collections import defaultdict
import numpy as np

subjects = { # Name: kword
    "Physics": "physic",
    "Chemistry": "chem",
    "Algebra": "alg",
    "Calculus": "calc",
    "English": "english",
    "History": "history",
    "Comp Sci": "comp",
    "Statistics": "stat"
}

gpa_map = {}
avg_map = defaultdict(dict)

found = set()

colors = ['blue', 'red', 'black', 'purple', 'orange', 'teal', 'green', 'maroon']

for index, row in cyranch_db.tables.rank.all().iterrows():

    gpa_map[row["user_id"]] = row["gpa"]

for index, row in cyranch_db.tables.grades.all().iterrows():

    if "AVG" in row["name"]:

        for name, kword in subjects.items():

            if kword in row["name"].lower():

                avg_map[name][row["user_id"]] = row["grade"]

                found.add(row["name"])

print("\n".join(sorted(found))) # Debug kword

def create_plot():
    """Plots with matplot lib"""
    import matplotlib.pyplot as plt

    f, subplots = plt.subplots(4, 2, sharex=True, sharey=True)

    plt.style.use('ggplot')

    subplots = np.ndarray.flatten(subplots) # B/c subplots is a matrix

    i = 0

    for subject in subjects:

        x, y = [], []

        for user in avg_map[subject]:

            if user in gpa_map:

                x.append(avg_map[subject][user])
                y.append(gpa_map[user])

        subplots[i].scatter(x, y, c=colors[i], marker='*')
        subplots[i].set_xlim([0, 110])
        subplots[i].set_ylim([3, 7])
        subplots[i].set_xlabel(subject)
        subplots[i].set_ylabel('GPA')

        i += 1

    f.suptitle('GPA vs Subject Avg')

    plt.show()

if __name__ == "__main__":

    create_plot()
