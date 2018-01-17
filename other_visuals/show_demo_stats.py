from cyranchdb import cyranch_db
from collections import defaultdict
import math

schools   = defaultdict(int)
genders   = defaultdict(int)
languages = defaultdict(int)
grades    = defaultdict(int)

for index, row in cyranch_db.tables.demo.all().iterrows():

    schools[row['school']] += 1
    genders[row['gender']] += 1
    languages[row['language']] += 1
    grades[str(row['gradelevel'])] += 1

def create_plot():
    """Plots with matplot lib"""
    import matplotlib.pyplot as plt

    def make_bar(plot, data_dict, title, limit=None, color=None, keys=None):

        if not keys:
            keys = sorted(data_dict.keys(), key=lambda key: -data_dict[key])

        if limit:
            keys = keys[:limit]

        indexes = list(range(len(keys)))

        plot.set_title(title)
        bars = plot.bar(indexes, [data_dict[k] for k in keys], color=color)
        plot.set_xticks(indexes)
        plot.set_xticklabels([k.title() for k in keys])

        for rect in bars:
            height = rect.get_height()
            plot.text(rect.get_x() + rect.get_width() / 2.,
                    height + 10,
                    '%d' % int(height),
                    ha='center', va='bottom')


    plt.style.use('ggplot')

    f, ((ax1, ax2, ax3, ax4)) = plt.subplots(4, 1)

    make_bar(ax1, schools, 'School', 5)
    make_bar(ax2, grades, 'Grade Level', keys=['12', '11', '10', '9'])
    make_bar(ax3, genders, 'Gender', color=['#E53935', '#3949AB'])
    make_bar(ax4, languages, 'Language', 5)

    plt.show()

if __name__ == "__main__":

    create_plot()
