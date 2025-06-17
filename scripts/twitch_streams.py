import dlt, requests
from dlt.destinations import filesystem
from datetime import datetime

CLIENT_ID = "w8pw2ef349exsdnstzuuymip2g8cf2"
CLIENT_SECRET = "cglivl5sw28u7bcpam2eoyan4d49o2"

def get_token():
    response = requests.post(
        "https://id.twitch.tv/oauth2/token",
        params={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )
    return response.json()["access_token"]

def fetch_all_streams(client_id, token):
    url = "https://api.twitch.tv/helix/streams"
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    pagination = None

    while True:
        params = {"first": 100}
        if pagination:
            params["after"] = pagination

        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()

        streams = data.get("data", [])
        pagination = data.get("pagination", {}).get("cursor")

        print(f"Fetched {len(streams)} streams with cursor: {pagination}")

        for stream in streams:
            stream["api_pagination_cursor"] = pagination
            stream["data_import_date"] = datetime.now().isoformat()
            yield stream

        if not pagination:
            break

@dlt.resource(
    name="twitch_streams",
    primary_key="id",
    table_name="twitch_streams",
    file_format="parquet"
)
def stream_resource_all():
    token = get_token()
    yield from fetch_all_streams(CLIENT_ID, token)

if __name__ == "__main__":
    fs_destination = filesystem("file:///C:/Users/User/twitch_bi/data")

    print(
        dlt.pipeline(
            "twitch_streams_pipeline",
            destination=fs_destination
        ).run(stream_resource_all())
    )
