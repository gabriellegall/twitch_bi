import glob
import os
import pandas as pd
from datetime import datetime, timezone

def model(dbt, session):
    dbt.config(
        materialized="incremental"
    )

    # List all .parquet files
    files = glob.glob('data/twitch_streams_pipeline_dataset/twitch_streams/*.parquet')

    # Exclude .parquet files already imported
    if dbt.is_incremental:
        imported_files = [row[0] for row in session.execute(f"SELECT DISTINCT file_name FROM {dbt.this}").fetchall()]
        files = [f for f in files if os.path.basename(f) not in imported_files]

    # Create a df of all .parquet files while keeping track of the [file_name]
    dfs = []
    import_timestamp = datetime.now(timezone.utc).isoformat()

    for f in files:
        df = session.read_parquet(f).to_df()
        file_name = os.path.basename(f)
        df['file_name']       = file_name
        df['file_name_date']  = datetime.fromtimestamp(float(file_name.split('.', 1)[0]))
        df['log_import_date'] = import_timestamp
        dfs.append(df)

    if dfs:
        final = pd.concat(dfs, ignore_index=True)
    else:
        # If no data to ingest, create an empty dataframe with the table's schema
        try:
            columns = [info[1] for info in session.execute(f"PRAGMA table_info('{dbt.this}')").fetchall()]
        except Exception:
            columns = []
        final = pd.DataFrame(columns=columns)

    return final
