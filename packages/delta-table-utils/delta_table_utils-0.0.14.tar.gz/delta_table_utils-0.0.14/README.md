# delta_table_utils

Delta table utilities.

The basic use case for this library is if you are working in Databricks and want to do upserts using [AutoLoader](https://docs.databricks.com/ingestion/auto-loader/index.html).

Basic usage:

```python
from delta_table.delta_table_utils import DeltaTableColumn, DeltaTable

schema_name = 'my_schema'
table_name = 'my_table'

# Define the delta table schema
column_list = [
    DeltaTableColumn('id', data_type='STRING', nulls_allowed=False, is_unique_id=True),
    DeltaTableColumn('col1', data_type='STRING', nulls_allowed=False),
    DeltaTableColumn('col2', data_type='DOUBLE'),
    DeltaTableColumn('col3', data_type='DOUBLE'),
    DeltaTableColumn('col4', data_type='DOUBLE'),
    DeltaTableColumn('created_at', data_type='TIMESTAMP'),
    DeltaTableColumn('updated_at', data_type='TIMESTAMP')
]

# Create the DeltaTable object
delta_table = DeltaTable(schema_name=schema_name, table_name=table_name, upload_path="<location_of_data_in_s3>", column_list=column_list)

# Create the table and start the stream
delta_table.create_if_not_exists(sqlContext)
delta_table.stream(spark, cloudFiles_format='csv')
```

## Additional notes

By default, when you use the `stream` method in this library, it stops as soon as no new data is detected. This is useful if you don't want a cluster running all the time and rather you just want to update your delta tables on some sort of a schedule.

