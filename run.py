import subprocess
import sys
import requests
from dotenv import load_dotenv
import os

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