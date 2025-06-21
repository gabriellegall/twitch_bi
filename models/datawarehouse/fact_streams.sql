{{ config(
    materialized='table'
) }}

SELECT 
  DATE(file_name_date) AS file_date,
  user_id,
  user_name,
  game_id,
  game_name,
  AVG(viewer_count) AS avg_viewer_count
FROM {{ ref('int_streams') }}
GROUP BY ALL