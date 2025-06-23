{{ config(
    materialized='table',
    unique_key=['file_name', 'id']
) }}

SELECT
    *
FROM {{ ref('stg_streams') }}
WHERE file_name_date >= CURRENT_DATE - INTERVAL '1' DAY

-- Deduplicate records
QUALIFY ROW_NUMBER() OVER (PARTITION BY file_name, id ORDER BY api_pagination_cursor DESC) = 1