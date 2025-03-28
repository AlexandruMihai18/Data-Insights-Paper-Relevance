import pandas as pd

def save_data_to_csv(pmids, gds_ids, gse_ids, texts, file_path):
	df = pd.DataFrame({
		'PMID': pmids,
		'GDS_ID': gds_ids,
		'GSE_ID': gse_ids,
		'Text': texts
	})
	df.to_csv(file_path, index=False)