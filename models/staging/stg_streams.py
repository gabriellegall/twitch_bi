import glob
import os
import pandas as pd
import datetime

def model(dbt, session):
    dbt.config(
        materialized="incremental"
    )

    ### PART 1 : Utility
    ### ----------------

    # Function to get the file_name from the path
    def get_file_name(file_path: str) -> str:
        return os.path.basename(file_path)

    # Function to get the file_name_date from the path
    def get_file_name_date(file_path: str) -> datetime.date:
        file_name = get_file_name(file_path)
        timestamp_str = file_name.split('.', 1)[0]
        return datetime.datetime.fromtimestamp(float(timestamp_str)).date()

    # PART 2 : Files filtering
    ### ----------------------

    # List all .parquet files
    files = glob.glob('data/twitch_streams_pipeline_dataset/twitch_streams/*.parquet')

    # If specified, keep only one specific date
    file_date_parameter = str(dbt.config.get("file_date"))

    if file_date_parameter != 'no_date_condition':
        try:
            file_date = datetime.datetime.strptime(file_date_parameter, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"file_date must be in YYYY-MM-DD format, got: {file_date_parameter}")        
        files = [f for f in files if get_file_name_date(f) == file_date]

    # Exclude .parquet files already imported
    if dbt.is_incremental:
        imported_files = [row[0] for row in session.execute(f"SELECT DISTINCT file_name FROM {dbt.this}").fetchall()]
        files = [f for f in files if get_file_name(f) not in imported_files]

    ### PART 3 : Merge all files
    ### ------------------------

    # Create a df of all .parquet files while keeping track of the [file_name]
    dfs = []
    import_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for f in files:
        df = session.read_parquet(f).to_df()
        df['file_name']       = get_file_name(f)
        df['file_name_date']  = get_file_name_date(f)
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