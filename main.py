import dataclasses

from matplotlib import pyplot as plt
from scipy.cluster._hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances

from processor.main import BookCollection
from scrapper.main import BibleScrapper

if __name__ == '__main__':
#     #scrap
#     # BibleScrapper()
#
#     #process
    bc = BookCollection()
#     b1 = list(bc.books.values())[0]
#     print(dataclasses.asdict(b1))
    print('hi')



    # Create the binary matrix where each word is a feature
    vectorizer = CountVectorizer(binary=True)
    word_matrix = vectorizer.fit_transform([i.clean_text for i in bc.books.values()])


    # Compute Jaccard distance between each pair of books
    distance_matrix = pairwise_distances(word_matrix, metric='jaccard')



    # Perform hierarchical clustering
    linkage_matrix = linkage(distance_matrix, method='ward')  # 'ward' is effective for creating hierarchical clusters

    # Plot dendrogram to visualize the "phylogenetic tree"
    plt.figure(figsize=(10, 7))
    dendrogram(linkage_matrix, labels=[i for i in bc.books], orientation="right")
    plt.title("Hierarchical Clustering of Books by Vocabulary")
    plt.xlabel("Distance")
    plt.show()
    #%%



