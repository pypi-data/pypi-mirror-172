# DOP Library

This package contains all the utils and functions that are used in the DOP
framework.


## run_results_to_bq
Takes a `run_results.json` file from either local storage or GCS and uploads it
to a BigQuery table using the included
[run_results table schema](/dop_library/run_results_table_schema.json).

It is important that the `run_results` table is created according to this
schema. If the schema doesn't match, the insertion might fail silently.

```python
from dop_library import run_results_to_bq

run_results_to_bq(
    run_results_path='gs://dbt-data/artifacts/run_results.csv',
    dest_dataset_id='dop_test',
    dest_table_id='run_results',
)
```

