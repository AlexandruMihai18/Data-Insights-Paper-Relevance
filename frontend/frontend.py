import dash
import requests

from dash import dcc, html, Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
	html.H1('PubMed Clustering'),
	html.Div([
		html.Label('Enter PMIDs (separated by space or endline):'),
		dcc.Input(id='pmids', type='text', value=''),
		html.Button('Cluster', id='cluster-button'),
	]),
	html.Div(id='plot-container')
])

@app.callback(
	Output('plot-container', 'children'),
	Input('cluster-button', 'n_clicks'),
	State('pmids', 'value')
)
def update_plot(n_clicks, pmids):
	if not n_clicks:
		return None
	
	pmids = pmids.split('\n')

	response = requests.post('http://localhost:5000/cluster', json={'pmids': pmids})
	plot_html = response.json().get('plot_html')

	return html.Iframe(srcDoc=plot_html, style={'width': '100%', 'height': '600px'})

if __name__ == '__main__':
	app.run(debug=True, port=3000)