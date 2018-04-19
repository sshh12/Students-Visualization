from cyranchdb import cyranch_db
from collections import defaultdict
import numpy as np
import math

users = defaultdict(dict)

for index, row in cyranch_db.tables.rank.all().iterrows():

    users[row["user_id"]]["gpa"] = row["gpa"]

for index, row in cyranch_db.tables.demo.all().iterrows():

    if row["gradelevel"] > 12 or row["user_id"] not in users:
        continue

    users[row["user_id"]]["lang"] = row["language"]
    users[row["user_id"]]["gender"] = row["gender"]
    users[row["user_id"]]["grade"] = str(row["gradelevel"])

def create_plot():
    """Plots with matplot lib"""
    import matplotlib.pyplot as plt

    def make_box(plot, users, category, labels, colors):

        x_datas = []

        for label in labels:

            x = []

            for user, data in users.items():
			
                if "lang" not in data: # filter incomplete demo data
                    continue

                if label.lower() in data[category]:
                    x.append(data["gpa"])

            x_datas.append(x)

        bplot = plot.boxplot(x_datas, notch=True, sym='+', patch_artist=True)
        plot.set_xticks(np.arange(1, len(labels) + 1))
        plot.set_xticklabels(labels)

        for patch, color in zip(bplot['boxes'], colors):
                patch.set_facecolor(color)

    plt.style.use('ggplot')

    f, ((ax1, ax2, ax3)) = plt.subplots(3, 1, sharey=True)

    f.suptitle('GPA Demographics')

    make_box(ax1, users, "lang", ['English', 'Spanish', 'Vietnamese', 'Arabic', 'Cantonese'], ['r', 'g', 'b', 'y', 'c'])

    make_box(ax2, users, "gender", ['Male', 'Female'], ['b', 'r'])

    make_box(ax3, users, "grade", ['10', '11', '12'], ['w', 'm', 'c'])

    plt.show()

if __name__ == "__main__":

    create_plot()
