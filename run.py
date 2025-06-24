import subprocess

subprocess.run(["python", "scripts/twitch_streams.py"], check=True)
subprocess.run(["dbt", "run"], check=True)