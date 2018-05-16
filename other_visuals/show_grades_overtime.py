from cyranchdb import cyranch_db
from collections import defaultdict
from math import factorial
import numpy as np

gradelevel_map = {}            # user -> gradelevel
grade_map = defaultdict(dict)  # gradelevel -> bin -> average

num_bins = 80
bin_range = (250000, 450000) # id range

def get_bin(x, num_bins=num_bins, bin_range=bin_range): # Find where x is given bins and range
    sidx, eidx = bin_range
    return int((x - sidx) / (eidx - sidx) * num_bins)

for index, row in cyranch_db.tables.demo.all().iterrows():

    gradelevel_map[row["user_id"]] = row["gradelevel"]

for index, row in cyranch_db.tables.grades.all().iterrows():

    if "AVG" not in row["name"] and row["user_id"] in gradelevel_map:

        gradelevel = gradelevel_map[row["user_id"]]

        bin = get_bin(row["id"])

        if bin < 0 or bin >= num_bins:
            continue

        if bin not in grade_map[gradelevel]:

            grade_map[gradelevel][bin] = []

        grade_map[gradelevel][bin].append(row["grade"])

# Calculate average for each bin

bin_averages = defaultdict(dict)

for gradelevel, bins in grade_map.items():

    for bin in bins.keys():

        bin_averages[gradelevel][bin] = np.mean(grade_map[gradelevel][bin])

# Smoothing

def savitzky_golay(y, window_size, order, deriv=0, rate=1): # http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay
    window_size = np.abs(np.int(window_size))
    order = np.abs(np.int(order))
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

def smooth(y):
    return savitzky_golay(y, window_size=39, order=5)

# Plot

def create_plot():
    """Plots with matplot lib"""
    import matplotlib.pyplot as plt

    colors = {
        9: 'y',
        10: 'r',
        11: 'g',
        12: 'b'
    }

    plt.style.use('ggplot')

    for gradelevel in [9, 10, 11, 12]:

        x, y = [], []

        for bin, avg in bin_averages[gradelevel].items():

            x.append(bin)
            y.append(avg)

        x, y = zip(*sorted(zip(x, y))) # Sort x, y by x
        x, y = np.array(x) / num_bins, smooth(np.array(y))

        plt.plot(x, y, colors[gradelevel] + '-', label=str(gradelevel), linewidth=1)

    plt.ylim(ymax=100, ymin=80)
    plt.legend(['9', '10', '11', '12'])
    plt.title('Avg. Grades Over Time')
    plt.ylabel('Avg. Grade')
    plt.xlabel('% of 2018 School Year ')

    plt.show()

if __name__ == "__main__":

    create_plot()
