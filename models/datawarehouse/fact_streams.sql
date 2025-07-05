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
{% set table_exists = check_table_exists(this) %}

SELECT
  -- Granuarity
  DATE(file_name_datetime)      AS file_name_date,
  TRY_CAST(user_id AS INT)      AS user_id,
  TRY_CAST(game_id AS INT)      AS game_id,
  -- Aggregations
  COUNT(DISTINCT file_name)     AS nb_files,
  ARRAY_AGG(DISTINCT file_name) AS file_names,
  AVG(viewer_count)             AS avg_viewer_count
FROM {{ ref('int_streams') }}

{% if not export_all and table_exists %} -- Incremental export
WHERE file_name_date >= (SELECT MAX(file_name_date) FROM {{ this }}) -- Overwrite on same-day (refresh)
{% endif %}

GROUP BY 1,2,3