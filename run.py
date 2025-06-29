import subprocess
import sys
import requests
from dotenv import load_dotenv
import os
from datetime import date, timedelta
import argparse

def run_default():
    """Run twitch_streams.py and dbt run normally."""

    load_dotenv()
    URL = os.getenv("HEALTHCHECK_URL")

    try:
        subprocess.run([sys.executable, "scripts/twitch_streams.py"], check=True)
        subprocess.run(["dbt", "run"], check=True)
        requests.get(URL, timeout=5)
        print("✅ Healthcheck ping sent successfully.")
    except Exception:
        requests.get(URL + "/fail", timeout=5)
        print("❌ Healthcheck failure ping sent.")
        raise

def dbt_iterative_reload(start_date: date, end_date: date):
    """
        Run dbt once per date in the given range using file_date.
        Technically, using dbt run --full-refresh would produce the same result, but this command may exceed memory limits on some machines.
        Furthermore, in some scenarios, it is necessary to reload the pipeline in a specific order (e.g. snapshots, incremental models checking previous state, etc.)    
    """
    load_dotenv()
    URL = os.getenv("HEALTHCHECK_URL")

    current_date = start_date
    while current_date <= end_date:
        date_str = str(current_date)
        print(f"📅 Running dbt for date: {date_str}")

        cmd = ["dbt", "run", "--vars", f'{{file_date: "{date_str}"}}']
        print(cmd)
        try:
            subprocess.run(
                cmd,
                check=True
            )

            requests.get(URL, timeout=5)
            print(f"✅ Healthcheck ping sent for {date_str}")

        except Exception:
            requests.get(URL + "/fail", timeout=5)
            print(f"❌ Healthcheck failure for {date_str}")
            raise

        current_date += timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run twitch_streams + dbt by default, or run dbt over a date range if start/end are provided."
    )
    parser.add_argument("--scenario"   , type=str, help="Confirm the scenario to execute: dbt_iterative_reload")
    parser.add_argument("--start_date" , type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end_date"   , type=str, help="End date in YYYY-MM-DD format")
    args = parser.parse_args()

    if args.scenario == 'dbt_iterative_reload' and args.start_date and args.end_date:
        start = date.fromisoformat(args.start_date)
        end = date.fromisoformat(args.end_date)
        dbt_iterative_reload(start, end)
    else:
        run_default()
