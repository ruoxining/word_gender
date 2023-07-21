import gensim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# please the parameters before using
# @param data_percent   percent of data to be plotted. total 30k. e.g. if data_percent = 10, 1/10 namely 3k data will be plotted
data_percent = 10


# plot germen word vector
def draw_words_3d(vectors, words, labels):

    tsne = TSNE(n_components=3, random_state=0)
    vectors3d = tsne.fit_transform(vectors)

    # draw image
    fig = plt.figure(figsize=(10,10))
    ax = Axes3D(fig)

    # data preprocessing
    # this block removes the extreme values so that the visualization more readable
    points = [point for point in vectors3d]
    points = sorted(points, key = lambda x:x[0])
    points = points[3:-3]
    points = sorted(points, key = lambda x:x[1])
    points = points[3:-3]
    points = sorted(points, key = lambda x:x[2])
    points = points[3:-3]

    # this block regularize the data so that the visualization more readable
    vector_1d = [point[0] for point in points]
    min1 = min(vector_1d)
    max1 = max(vector_1d)
    vector_2d = [point[1] for point in points]
    min2 = min(vector_2d)
    max2 = max(vector_2d)
    vector_3d = [point[2] for point in points]
    min3 = min(vector_3d)
    max3 = max(vector_3d)

    # this block plots the data
    for index in range(len(points)):
        ax.scatter((vector_1d[index] - min1)/(max1 - min1),(vector_2d[index] - min2)/(max2 - min2),(vector_3d[index] - min3)/(max3 - min3), s=30, c='r' if labels[index] == 'm' else 'b' if labels[index] == 'f' else 'grey', alpha=0.5)
    fig.legend()

    # this block make animation and saves the .gif file
    angle = 3
    def rotate(angle):
        ax.view_init(azim=angle)
    ani = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 360, angle), interval=50)
    ani.save('german/tsne3k.gif', writer=animation.PillowWriter(fps=20))


# get trained model
model = gensim.models.KeyedVectors.load_word2vec_format("german/vector/german.model", binary=True)

## make label
vectors = []
words = []
labels = []
with open("german/gender/german_gender.txt", "r") as label_file:
    texts = label_file.readlines()
    index = 0
    for line in texts:
        line = line.split(' ')
        try:
            if (index % data_percent == 0):
                vectors.append(model[str(line[0])])
                words.append(str(line[0]))
                labels.append(line[1][1])
        except:
            pass
        index += 1

draw_words_3d(vectors, words, labels, True, False, -3, 3, -1.5, 2.5, r'$Word\ Gender$')