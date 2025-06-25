{# More info about the config : https://duckdb.org/docs/stable/sql/statements/copy.html#copy--to-options #}
{{ config(
    materialized='external',
    format='parquet',
    location='data/fact_streams.parquet',
    options={
        "partition_by": "file_name_date",
        "overwrite_or_ignore": true
    }
  )
}}

{% set export_all = var("export_all", false) %}

SELECT
  DATE(file_name_date)      AS file_name_date,
  COUNT(DISTINCT file_name) AS nb_files,
  TRY_CAST(user_id AS INT)  AS user_id,
  TRY_CAST(game_id AS INT)  AS game_id,
  AVG(viewer_count)         AS avg_viewer_count
FROM {{ ref('int_streams') }}

-- Full export of all .parquet files
{% if not export_all %}
WHERE file_name_date >= CURRENT_DATE - INTERVAL '2' DAY
{% endif %}

GROUP BY ALL