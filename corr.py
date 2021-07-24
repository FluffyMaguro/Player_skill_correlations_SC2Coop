import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patheffects as path_effects
from scipy.stats.stats import pearsonr, linregress

# LOAD DATA
with open('data.json', 'r') as f:
    a = json.load(f)


def check(i):
    return i[1] > 90 and i[2] > 0


kills = np.array([i[0] for i in a if check(i)])
level = np.array([i[1] for i in a if check(i)])
apm = np.array([i[2] for i in a if check(i)])

i = 0


def add_subplot(axis, x, y, xlabel, ylabel, title):
    global i

    pear = pearsonr(x, y)
    reg = linregress(x, y)

    axis[i].grid(color='#ddd',
                 zorder=0)  # Putting grid behind with forced zorder
    axis[i].scatter(x, y, s=0.4, zorder=2)
    axis[i].set_xlabel(xlabel)
    axis[i].set_ylabel(ylabel)
    axis[i].set_title(title)

    # Regression
    axis[i].plot(
        x,
        reg.slope * x + reg.intercept,
        c='brown',
        label=f'Linear regression: {reg.slope:.3e}*x + {reg.intercept:.2f}')
    # Legend
    axis[i].legend(loc="upper right", facecolor='#ddd')

    # Format for percents
    if max(y) < 1.5:
        yformat = mtick.FuncFormatter("{:.0%}".format)
        axis[i].yaxis.set_major_formatter(yformat)

    # Fix ylim for APM
    if max(y) > 100:
        axis[i].set_ylim([0, 200])

    # Data correlation
    xpos = (axis[i].get_xlim()[1] -
            axis[i].get_xlim()[0]) * 0.02 + axis[i].get_xlim()[0]

    effects = [
        path_effects.SimplePatchShadow(offset=(0.5, -0.5),
                                       alpha=1,
                                       shadow_rgbFace='#eee'),
        path_effects.Normal()
    ]

    color = '#333'
    text = axis[i].text(xpos,
                        axis[i].get_ylim()[1] * 0.85,
                        f'Correlation: {pear[0]:.3f}',
                        fontsize=16,
                        c=color,
                        path_effects=effects)

    # Data p-value
    axis[i].text(xpos,
                 axis[i].get_ylim()[1] * 0.78,
                 f'p-value: {pear[1]:.3e}',
                 fontsize=10,
                 c=color,
                 path_effects=effects)

    # Facecolor
    axis[i].set_facecolor('#eee')
    # Update index
    i += 1


def get_graphs():
    fig, axis = plt.subplots(3, 1, figsize=(10, 10))

    # APM - KILLS
    add_subplot(axis=axis,
                x=apm,
                y=kills,
                xlabel='Player APM',
                ylabel='Percent of kills',
                title="Percent of kills / APM")

    # LEVEL - KILLS
    add_subplot(axis=axis,
                x=level,
                y=kills,
                xlabel='Player ascension level',
                ylabel='Percent of kills',
                title="Percent of kills / player ascension level")

    # Level - APM
    add_subplot(axis=axis,
                x=level,
                y=apm,
                xlabel='Player ascension level',
                ylabel='Player APM',
                title="APM / player ascension level")

    # Figure title
    fig.suptitle(
        'Correlations between ascension levels (91–1000), APM and percentage of kills',
        fontsize=16)

    plt.tight_layout(h_pad=2)  # Padding between plots
    plt.subplots_adjust(top=0.91)  # Adjust title padding
    plt.savefig('corr.png')
    # plt.show()


def get_heatmap():
    corr_matrix = np.corrcoef([level, apm, kills])

    fig, ax = plt.subplots()
    im = ax.imshow(corr_matrix)
    im.set_clim(-1, 1)
    ax.grid(False)

    names = ('Level', 'APM', 'Kills')
    ax.xaxis.set(ticks=(0, 1, 2), ticklabels=names)
    ax.yaxis.set(ticks=(0, 1, 2), ticklabels=names)
    ax.set_ylim(2.5, -0.5)
    for i in range(3):
        for j in range(3):
            ax.text(j,
                    i,
                    f"{corr_matrix[i, j]:.2f}",
                    ha='center',
                    va='center',
                    color='black')
    cbar = ax.figure.colorbar(im, ax=ax, format='% .2f')
    plt.savefig('heatmap.png')
    # plt.show()


get_graphs()
# get_heatmap()