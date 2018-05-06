from cyranchdb import cyranch_db
from collections import defaultdict
import math

user_map = {}                  # user id -> school, grade, gender
gpas_map = {}                  # user id -> pos, gpa

for index, row in cyranch_db.tables.demo.all().iterrows():

    if row["gradelevel"] > 12:
        continue

    user_map[row.user_id] = {
        "gender": row["gender"],
        "language": row["language"]
    }

for index, row in cyranch_db.tables.rank.all().iterrows():

    gpas_map[row["user_id"]] = (row["pos"], row["gpa"])

def create_plot():
    """Plots with matplot lib"""
    import matplotlib.pyplot as plt

    def create_scatter_plot(plot, feature, values, color_map):

        feature_sets = {val: [] for val in values}

        for user in user_map:
            if user in gpas_map and user_map[user][feature] in values:
                feature_sets[user_map[user][feature]].append(gpas_map[user])

        for val in values:

            x, y = [], []

            for pos, gpa in feature_sets[val]:
                x.append(int(pos))
                y.append(float(gpa))

            plot.scatter(x, y, c=color_map[val], marker='.')
            plot.legend(values)
            plot.set_ylabel("GPA")
            plot.set_xlabel("Rank")

    f, ((ax1, ax2)) = plt.subplots(2, 1, sharey=True)

    plt.style.use('ggplot')

    create_scatter_plot(ax1, "gender",
                        ["male", "female"],
                        {"male": "b", "female": "r"})

    create_scatter_plot(ax2, "language",
                        ["english", "spanish", "vietnamese", "arabic", "cantonese"],
                        {"english": "r", "spanish": "g", "vietnamese": "b", "arabic": "y", "cantonese": "c"})

    f.suptitle('GPA Gender/Language')

    plt.show()

if __name__ == "__main__":

    create_plot()
