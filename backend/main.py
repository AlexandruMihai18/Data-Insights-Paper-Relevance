from flask import Flask, request, jsonify
from fetch_data import fetch_gds_ids, fetch_dataset_texts
from clustering import cluster_texts
from visualization import generate_plot

app = Flask(__name__)

@app.route('/cluster', methods=['POST'])
def cluster_pmids():
	data = request.json

	print('Gatering data...')

	pmids = data.get('pmids', [])

	if not pmids:
		return jsonify({'error': 'No PMIDs provided'}), 400

	print('Fetching GDS IDs...')

	pmid_to_gds = {pmid: fetch_gds_ids(pmid) for pmid in pmids}

	print('Fetching dataset texts...')

	pmids, dataset_texts = fetch_dataset_texts(pmid_to_gds)

	print('Clustering...')

	clusters, embeddings = cluster_texts(dataset_texts)

	print('Generating plot...')

	plot_html = generate_plot(embeddings, clusters, pmids)

	return jsonify({'plot_html': plot_html})

if __name__ == '__main__':
	app.run(debug=True, port=5000)
	