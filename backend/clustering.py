from sklearn.feature_extraction.text import TfidfVectorizer
from gapstatistics.gapstatistics import GapStatistics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def cluster_texts(texts):
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(texts)
	
	pca = PCA(n_components=2)
	embeddings = pca.fit_transform(X.toarray())

	gs = GapStatistics(distance_metric='euclidean')
	optimum = gs.fit_predict(K=10, X=X.toarray(), n_iterations=30)

	kmeans = KMeans(n_clusters=optimum, random_state=42)
	clusters = kmeans.fit_predict(X)
	
	return clusters, embeddings
