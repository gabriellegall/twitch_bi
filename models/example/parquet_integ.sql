{{ config(materialized='table') }}

SELECT * FROM parquet_scan('data/snapshots/twitch_streams_all/*.parquet')