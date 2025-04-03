# Data-Insights-Paper-Relevance

## Project Structure

```
├── backend
│   ├── clustering.py
│   ├── Dockerfile
│   ├── fetch_data.py
│   ├── main.py
│   ├── requirements.txt
│   ├── save_data.py
│   └── visualization.py
├── frontend
│   ├── Dockerfile
│   ├── frontend.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## How to run the project

Make sure you have Docker and Docker Compose installed on your device.

You can run the project by deploying Docker containers:

```
docker compose up
```

You can then access the website at: http://0.0.0.0:3000


## Test the project

The project expects a list of PMIDs separated by spaces.

After extracting the text data from GEO datasets. It will concatenate
the results and perform the tf-idf algorithm in order to construct
vector representation of the text. After that it will determine the
best number of clusters and perform clustering using KMeans algorithm.

The visualization was made using the PCA algorithm, extracting the 2 components
that allow visualization in a 2D space.

## Further mentions

In `backend/fetch_data.py` there are 2 options for fetching the required data.
One of the is using the eutils API (`fetch_dataset_text_v2`) and the
other is done by scraping the GEO datasets official website (`fetch_dataset_text_v1`).

There are 2 important differences when considering these 2 alternative:

* Time wise, v2 performs about 30% better than v1, as it does not require
to process entire webpages to find meaningful data

* v2 disregards the Overall design text field, as it is not provided
using the eutils API.