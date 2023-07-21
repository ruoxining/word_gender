import gensim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# please the parameters before using
# @param isPCA   True if use PCA, False if use t-SNE
isPCA = True
# @param data_percent   percent of data to be plotted. total 30k. e.g. if data_percent = 10, 1/10 namely 3k data will be plotted
data_percent = 10


# function draw_words
def draw_words_2d(vectors, words, labels, pca=False, alternate=True, arrows=True, x1=3, x2=3, y1=3, y2=3, title=''):

    if pca:
        pca = PCA(n_components=2, whiten=True)
        vectors2d = pca.fit(vectors).transform(vectors)
    else:
        tsne = TSNE(n_components=2, random_state=0)
        vectors2d = tsne.fit_transform(vectors)

    # draw image
    plt.figure(figsize=(6,6))
    if pca:
        plt.axis([x1, x2, y1, y2])

    for index, point, word in zip(range(len(words)), vectors2d , words):
        # plot points
        plt.scatter(point[0], point[1], c='r' if labels[index] == 'm' else 'b' if labels[index] == 'f' else 'grey')
        # plot word annotations
        if index%100 == 0:     # add labels to 1/1000
            plt.annotate(word, xy = (point[0], point[1]), xytext = (7, -6), textcoords = 'offset points', ha = 'left', va = 'bottom', size = "x-large")

    # draw arrows
    if arrows:
        for i in range(0, len(words)-1, 2):
            a = vectors2d[i][0] + 0.04
            b = vectors2d[i][1]
            c = vectors2d[i+1][0] - 0.04
            d = vectors2d[i+1][1]
            plt.arrow(a, b, c-a, d-b,shape='full',lw=0.1,edgecolor='#bbbbbb',facecolor='#bbbbbb',length_includes_head=True,head_width=0.08,width=0.01)

    # draw diagram title
    if title:
        plt.title(title)

    plt.tight_layout()
    plt.show()


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

draw_words_2d(vectors, words, labels, isPCA, True, False, -3, 3, -1.5, 2.5, r'$Word\ Gender$')