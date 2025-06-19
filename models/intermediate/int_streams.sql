{{ config(
    materialized='table'
) }}

SELECT 
    *
FROM {{ ref('stg_streams') }}
QUALIFY ROW_NUMBER() OVER (PARTITION BY file_name, id ORDER BY data_import_date DESC) = 1