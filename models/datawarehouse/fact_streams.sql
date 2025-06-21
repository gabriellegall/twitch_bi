{{ config(
    materialized='external',
    format='parquet',
    location='data\fact_streams.parquet',
    options={
        "partition_by": "file_date",
        "overwrite": True
    }
  )
}}

SELECT
  DATE(file_name_date)      AS file_date,
  TRY_CAST(user_id AS INT)  AS user_id,
  TRY_CAST(game_id AS INT)  AS game_id,
  AVG(viewer_count)         AS avg_viewer_count
FROM {{ ref('int_streams') }}
GROUP BY ALL