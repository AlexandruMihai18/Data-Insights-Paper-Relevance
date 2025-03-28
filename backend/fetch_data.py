import requests
import re
import pandas as pd

from bs4 import BeautifulSoup

def fetch_gds_ids(pmid):
	url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=gds&linkname=pubmed_gds&id={pmid}&retmode=xml'
	response = requests.get(url)
	
	soup = BeautifulSoup(response.text, 'xml')
	links = soup.find_all('Link')
	gds_ids = [link.Id.text for link in links]
	return gds_ids

def fetch_dataset_text_v1(gds_id):
	url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&id={gds_id}&retmode=xml'
	response = requests.get(url)

	gse_tag = re.compile(r'Accession: GSE\d+').search(response.text)
	if not gse_tag:
		return None, None
	
	gse_tag = gse_tag.group()
	gse_id = gse_tag.split(': ')[1]

	url = f'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse_id}'
	response = requests.get(url)

	soup = BeautifulSoup(response.text, 'html.parser')

	title = find_field_v1(soup, 'Title')
	organism = find_field_v1(soup, 'Organism')
	experiment_type = find_field_v1(soup, 'Experiment type')
	summary = find_field_v1(soup, 'Summary')
	overall_design = find_field_v1(soup, 'Overall design')

	return gse_id, f'{title} {organism} {experiment_type} {summary} {overall_design}'

def fetch_dataset_text_v2(gds_id):
	url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id={gds_id}&retmode=xml'
	response = requests.get(url)

	soup = BeautifulSoup(response.text, 'xml')

	title = find_field_v2(soup, 'title')
	organism = find_field_v2(soup, 'taxon')
	experiment_type = find_field_v2(soup, 'gdsType')
	summary = find_field_v2(soup, 'summary')
	overall_design = find_field_v2(soup, 'overallDesign')

	gse_id = find_field_v2(soup, 'GSE')
	gse_id = f'GSE{gse_id}' if gse_id else None

	return gse_id, f'{title} {organism} {experiment_type} {summary} {overall_design}'

def find_field_v1(soup, field_name):
	field_tag = soup.find('td', text=field_name)
	
	if not field_tag:
		return None

	if not field_tag.find_next('td'):
		return None

	return field_tag.find_next('td').text

def find_field_v2(soup, field_name):
	field_tag = soup.find('Item', Name=field_name)
	if not field_tag:
		return None
	
	return field_tag.text

def fetch_dataset_texts(pmid_gds):
	pmids = []
	gsd_ids = []
	gse_ids = []
	dataset_texts = []

	for pmid, gds_ids in pmid_gds.items():
		for gds_id in gds_ids:
			gse_id, dataset_text = fetch_dataset_text_v2(gds_id)
			if dataset_text:
				pmids.append(pmid)
				gsd_ids.append(gds_id)
				gse_ids.append(gse_id)
				dataset_texts.append(dataset_text)

	return pmids, gsd_ids, gse_ids, dataset_texts
	