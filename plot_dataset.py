import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt

confused_vals = np.loadtxt("data_c.csv", delimiter=",")
non_confused_vals = np.loadtxt("data_n.csv", delimiter=",")

joined = np.concatenate((confused_vals, non_confused_vals))

tsne = TSNE(n_components=3)
pcaed = tsne.fit_transform(joined)

confused_pca = joined[:len(confused_vals)]
non_confused_pca = joined[len(confused_vals):]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(confused_pca[:, 0], confused_pca[:, 1], confused_pca[:, 2], label="Confused")
ax.scatter(non_confused_pca[:, 0], non_confused_pca[:, 1], non_confused_pca[:, 2], label="Non Confused")

plt.legend()
plt.show()
