# ⚡ Overview

## Purpose
This project is a PoC for a serverless data processing pipeline using DuckDB and DBT. It transforms raw Twitch data from Parquet files into analysis-ready reporting tables, which are also saved in Parquet format. 
While the PoC uses a local folder `/data` for output files, the architecture could be compatible with a cloud environment like AWS S3, GCP, or Azure Blob Storage, allowing cloud BI tools to query the data directly. For instance, we can imagine to import the reporting Parquet files from Azure Blob Storage into a Power BI Semantic Model using PowerQuery.

The main benefits are :
- **Massive cost reduction**: cloud storage cost is close to zero, DuckDB and DBT are free, only pay for the VM compute time of the regular batches.
- **Decoupled and future-proof architecture**: the compute layer can be switched out without any migration effort. On the storage side, the Parquet file format is not locked into a proprietary format and a wide ecosystem of tools can read it directly.
- **Time-to-market and agility**: this project is extremely light and quick to deploy. It can even serve as an interim data lakehouse solution before scaling to a cloud datawarehouse like Snowflake or BigQuery. Since all the transformations are in DBT, the technical migration effort from DuckDB is marginal.

## Repository
This repository contains all the scripts aiming to: 
1. Call the Twitch API to get all currently live streams and save the results in a Parquet file under `/data/twitch_streams_pipeline`.
2. Run DBT on DuckDB to ingest, transform and store this raw data.
3. Output a transformed reporting table `fact_streams` under `/data`.

# 🛠️ Technical overview
## Tools
- Data extraction (API): **Python** (with [DLT - Data Load Tool library](https://dlthub.com))
- Data storage & compute: **DuckDB** (on Docker)
- Data transformation: **DBT** (on Docker)
- Documentation: **DBT Docs**
- Deployment: using **Docker Hub**
- Pipeline monitoring: [**Healthcheck.io**](https://healthchecks.io/)

## Requirements
- Python
- Docker
- Makefile

### Optional
- DuckDB CLI

## Commands
This project is fully dockerized and can be executed locally or deployed on a server.

### Local execution
...

### Virtual Private Server (VPS) deployment
Here is how to deploy the project on a VPS:
1. In an Ubuntu machine, create a new project: `mkdir ~/twitch_bi`.
2. Inside, create a `/data` folder: `mkdir data`.
3. Pull and run the docker image with a bind-mount the `/data` folder.
```bash
docker pull gabriellegall/twitch-bi:latest
docker run --rm -it -v "$(pwd)/data:/app/data" gabriellegall/twitch-bi:latest
```

# 📂 Project

## Data extraction
The script `twitch_streams.py` ingests real-time stream data from the Twitch API. Using the DLT library, it retrieves a **snapshot** of all active streams at the time of execution. The script navigates the API's paginated results using a cursor and persists the extracted data into a single Parquet file, which is stored in the `/data` directory. The Parquet file is suffixed with the execution time of the pipeline (i.e. the snapshot date).
