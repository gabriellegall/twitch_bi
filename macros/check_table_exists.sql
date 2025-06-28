{% macro check_table_exists(relation) %}

    {% set relation_exists = adapter.get_relation(
        database=relation.database,
        schema=relation.schema,
        identifier=relation.identifier
    ) is not none %}
    
    {{ return(relation_exists) }}

{% endmacro %}