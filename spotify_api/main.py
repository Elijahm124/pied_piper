import json

import requests
from secrets1 import *
import base64
import sys

# curl -X

auth_url = "https://accounts.spotify.com/api/token"

auth_header = {}
auth_data = {}


# Base64 Encode CLient ID & CLient Secret
def get_access_token(client_id, client_secret):
    message = f"{client_id}:{client_secret}"
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base_64_message = base64_bytes.decode("ascii")

    auth_header["Authorization"] = f"Basic {base_64_message}"
    auth_data["grant_type"] = "client_credentials"

    res = requests.post(auth_url, headers=auth_header, data=auth_data)

    response_object = res.json()
    # print(json.dumps(response_object, indent=2))

    access_token = response_object["access_token"]

    return access_token


def get_playlist_tracks(token, playlist_id):
    playlist_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"

    get_header = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(playlist_endpoint, headers=get_header)

    playlist_object = res.json()

    return playlist_object


token = get_access_token(client_id, client_secret)

playlist_id = "4mOomMjwRCpimORh5IEBJy?si=031149c527db438a"

tracklist = get_playlist_tracks(token, playlist_id)

# print(tracklist)

#print(tracklist["tracks"]["items"][0]["track"]["album"]["name"])


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def iterjsoon(f):
    for key in f.keys():
        if (isinstance(f[key], dict)):
            uprint(key, ":")
            print("{")
            iterjsoon(f[key])
            print("}")
        else:
            uprint(key, ":", f[key])
#iterjsoon(tracklist)
print(json.dumps(tracklist, indent=2))
