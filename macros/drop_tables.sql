{% macro drop_tables(schema='main', table_name_ilike='dbt_tmp') %}
    {%- set query %}
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{{ schema }}'
          AND table_type = 'BASE TABLE'
          AND table_name ILIKE '%{{ table_name_ilike }}%'
    {%- endset %}

    {% if execute %}
        {# {% do log("Compiled query: " ~ query, info=True) %} #}
        {%- set results = run_query(query) %}
        {%- set table_names = results.columns[0].values() %}
        {%- for table in table_names %}
            {% set drop_sql = "DROP TABLE IF EXISTS " ~ schema ~ "." ~ table ~ " CASCADE" %}
            {% do log("Executed: " ~ drop_sql, info=True) %}
            {% do run_query(drop_sql) %}
        {%- endfor %}
    {% endif %}
{% endmacro %}
