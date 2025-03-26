import plotly.express as px
import pandas as pd

def generate_plot(embeddings, clusters, pmids):
	df = pd.DataFrame({
		'X': embeddings[:, 0],
		'Y': embeddings[:, 1],
		'Cluster': clusters,
		'PMID': pmids
	})

	fig = px.scatter(df, x='X', y='Y', color=df['Cluster'].astype(str), hover_data=df['PMID'])

	return fig.to_html()