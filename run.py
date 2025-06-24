import subprocess
import sys

subprocess.run([sys.executable, "scripts/twitch_streams.py"], check=True)
subprocess.run(["dbt", "run"], check=True)