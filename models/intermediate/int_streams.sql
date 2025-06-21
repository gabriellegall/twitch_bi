{{ config(
    materialized='incremental',
    unique_key=['file_name', 'id']
) }}

SELECT
    *
FROM {{ ref('stg_streams') }}

-- Process only recent data
{% if is_incremental() %}
WHERE file_name_date >= CURRENT_DATE - INTERVAL '30' DAY
{% endif %}

-- Deduplicate records
QUALIFY ROW_NUMBER() OVER (PARTITION BY file_name, id ORDER BY api_pagination_cursor DESC) = 1