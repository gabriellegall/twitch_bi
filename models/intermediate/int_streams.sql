{{ config(
    materialized='incremental',
    unique_key=['file_name', 'id']
) }}

SELECT
    *
FROM {{ ref('stg_streams') }}

-- Incremental load
{% if is_incremental() %}
WHERE file_name_date > (SELECT MAX(file_name_date) FROM {{ this }})
{% endif %}

-- Deduplicate records
QUALIFY ROW_NUMBER() OVER (PARTITION BY file_name, id ORDER BY api_pagination_cursor DESC) = 1