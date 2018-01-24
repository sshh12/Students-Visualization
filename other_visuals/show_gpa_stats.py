from cyranchdb import cyranch_db
from collections import defaultdict
import math

user_map = {}                  # user id -> school, grade
gpas_map = defaultdict(list)   # class#  -> [(pos, gpa, user id), ...]
class_map = {}                 # class#  -> class names

for index, row in cyranch_db.tables.demo.all().iterrows():

    user_map[row.user_id] = (row["school"], int(row["gradelevel"]))

for index, row in cyranch_db.tables.rank.all().iterrows():

    gpas_map[str(row["classsize"])].append((row["pos"],
                                            row["gpa"],
                                            row["user_id"]))

for class_ in gpas_map:

    # Fix db rows by using the latest (highest) grade levels
    grade_levels = [user_map[user_id][1] for _, _, user_id in gpas_map[class_]]
    actual_grade_level = int(math.ceil(sum(grade_levels) / float(len(grade_levels))))

    class_map[class_] = user_map[gpas_map[class_][0][2]][0] + "##" + str(actual_grade_level)

classes = [class_map[v] for v in class_map]

def print_for_google_sheets():
    """Prints data in a format that can be used in gsheets"""
    print("{},{}".format("pos", ",".join(classes)))

    for class_ in class_map:

        for pos, gpa, _ in gpas_map[class_]:

            columns = [""] * len(classes)
            columns[classes.index(class_map[class_])] = str(gpa)
            print("{},{}".format(pos, ",".join(columns)))

def create_plot():
    """Plots with matplot lib"""
    import matplotlib.pyplot as plt

    def get_school_color(school):
        if "Ranch" in school:
            return "#202c85"
        if "Cy-Fair" in school:
            return "#652325"
        elif "Jersey Village" in school:
            return "#4d2d78"
        elif "Woods" in school:
            return "#c6ab16"
        elif "Ridge" in school:
            return "#1B5E20"
        elif "Falls" in school:
            return "#81C784"
        elif "Langham" in school:
            return "#B71C1C"
        elif "Springs" in school:
            return "#E91E63"
        else:
            return "#000000"

    markers = {
        '9' : 'o',
        '10': '+',
        '11': '.',
        '12': '*'
    }

    legend = []

    plt.style.use('ggplot')

    for class_ in sorted(class_map, key=lambda key: class_map[key]):

        x, y = [], []

        for pos, gpa, _ in gpas_map[class_]:
            x.append(int(pos))
            y.append(float(gpa))

        school, grade = class_map[class_].split("##")

        legend.append(school.title().replace("High School", "") + " " + grade)

        plt.scatter(x, y, c=get_school_color(school), marker=markers[grade], label=school)

    plt.legend(legend)
    plt.yticks([3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7])
    plt.ylabel('GPA')
    plt.xlabel('Class Rank')
    plt.title('CFISD GPAs')
    plt.show()

if __name__ == "__main__":

    create_plot()
