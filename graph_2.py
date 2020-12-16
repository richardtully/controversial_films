import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_pickle('EL_IMDb_calculations.pkl')
df = df[df.scores != 'Error']
df = df.sort_values('votes', ascending = False)[:500]
df = df.sort_values('mean', ascending = False)

ratios_dict = df.ratios.to_dict()

name = '500 most voted for movies ordered by mean rating'


category_names = [str(i) for i in range(1,11)]
results = ratios_dict


def build_graph(results, category_names):

    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('Spectral')(
        np.linspace(0, 1, data.shape[1]))

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.invert_yaxis()
    ax.xaxis.set_visible(True)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    plt.xlabel('Ratio of each rating')
    plt.ylabel('500 movies')


    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        labels = [i for i in range(len(ratios_dict))]
        # labels = [i*0.1 for i in labels]
        ax.barh(labels, widths, left=starts, height=1,
                label=colname, color=color)
        xcenters = starts + widths / 2

    ax.legend(title = 'Rating',ncol=1, bbox_to_anchor=(1,1),
              loc='best', fontsize='small')

    return fig, ax


build_graph(results, category_names)
plt.title(name)
plt.show()