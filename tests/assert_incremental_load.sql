WITH stg_file_count AS (
    SELECT COUNT(DISTINCT file_name) AS count_files FROM {{ ref('stg_streams') }}
)

, int_file_count AS (
    SELECT COUNT(DISTINCT file_name) AS count_files FROM {{ ref('int_streams') }}
)

, prod_file_count AS (
    SELECT COUNT(DISTINCT file_name) AS count_files FROM {{ ref('fact_streams') }} CROSS JOIN UNNEST(file_names) AS t(file_name)
)

SELECT
    stg_file_count.count_files AS stg_count_files,
    int_file_count.count_files AS int_count_files,
    prod_file_count.count_files AS prod_count_files,
FROM stg_file_count
    CROSS JOIN int_file_count
    CROSS JOIN prod_file_count
WHERE TRUE 
    AND int_file_count.count_files  != stg_file_count.count_files
    OR prod_file_count.count_files  != stg_file_count.count_files
