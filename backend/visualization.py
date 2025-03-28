import plotly.express as px
import pandas as pd

def generate_plot(embeddings, clusters, pmids, gsd_ids, gse_ids):
	df = pd.DataFrame({
		'X': embeddings[:, 0],
		'Y': embeddings[:, 1],
		'GDS_ID': gsd_ids,
		'GSE_ID': gse_ids,
		'Cluster': clusters,
		'PMID': pmids
	})

	df['PMID'] = df['PMID'].astype(str)

	fig = px.scatter(
		df,
		x='X',
		y='Y',
		color='Cluster',
		hover_data=['PMID', 'GDS_ID', 'GSE_ID'],
		title='PMID Clustering'
	)

	return fig.to_html()