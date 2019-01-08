import json
from glob import glob
import os
import urllib.parse

import networkx as nx

from rus_rap.preprocessing import text_stemming
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.manifold import MDS

MDS()

DIR_PATH_TEXTS = ".\\textsByArtist"
DIR_PATH_WORDS = ".\\sortWordFreq"

textArtist = dict()


def getWordSet(filename):
    result = set()
    file = open(DIR_PATH_WORDS + "\\" + filename)
    for line in file:
        result.add(line.split(" ")[0])
    return result


for path in glob(os.path.join(os.path.expanduser(DIR_PATH_TEXTS), '*.json')):
    nameFile = os.path.basename(path)[:os.path.basename(path).rfind('.')]  # without extension
    print(nameFile)
    file = open(path, mode="r", encoding="maccyrillic")
    data = json.load(file)
    artist = urllib.parse.unquote(data["artist"]).encode('maccyrillic').decode('utf-8')
    wordSet = getWordSet(nameFile)

    texts = list()
    print(len(data['texts']))
    for text in data['texts']:
        texts.append(text_stemming(urllib.parse.unquote(text).encode('maccyrillic').decode('utf-8', errors="ignore"),
                                   wordDict=wordSet))
    textArtist[artist] = " ".join(texts)

listArt = np.array(list(textArtist.items()))
print(listArt)

tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=200000,
                                   min_df=0.1,
                                   use_idf=True, ngram_range=(1, 1))

tfidf_matrix = tfidf_vectorizer.fit_transform(listArt[:, 1])
print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()
print(terms)
dist = 1 - cosine_similarity(tfidf_matrix)
print(dist)

G = nx.Graph()

for i in range(len(dist)):
    for j in range(i + 1, len(dist)):
        G.add_edge(listArt[i, 0], listArt[j, 0], weight=dist[i][j])

nx.drawing.nx_pylab.draw_kamada_kawai(G, edge_color="#FFFFFF", with_labels=True)

# mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
# pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
# xs, ys = pos[:, 0], pos[:, 1]
# print(xs)
# print(ys)
#
# df = pd.DataFrame(dict(x=xs, y=ys, name=listArt[:, 0]))
#
# df.to_csv("results.csv", sep='\t', encoding='utf-8')
#
# fig, ax = plt.subplots(figsize=(17, 9)) # set size
# ax.margins(0.05)
#
# for index, row in df.iterrows():
#     ax.plot(row['x'], row['y'], marker='o', linestyle='', ms=12, color='#66ff99', mec='none')
#     ax.set_aspect('auto')
#     ax.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
#     ax.tick_params(axis='y', which='both', left='off', top='off', labelleft='off')
#
# for i in range(len(df)):
#     ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['name'], size=8)
#
# plt.show()
