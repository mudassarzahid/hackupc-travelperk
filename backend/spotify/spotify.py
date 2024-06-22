import collections
from typing import Any, Optional

import pandas as pd
import requests
from requests import Response

from utils.consts import QUEUE_CACHE_SIZE

LIMIT = 50


class Spotify:
    API_URL = "https://api.spotify.com/v1"

    def __init__(self, token):
        self.token = token
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token),
        }
        self.queue = collections.deque([], QUEUE_CACHE_SIZE)

    def get_saved_tracks(self) -> Response:
        response = requests.get(
            self.API_URL + "/me/tracks",
            headers=self.headers,
            params={"limit": 50},
        )

        return response

    def get_recent_tracks(self) -> Response:
        response = requests.get(
            self.API_URL + "/me/player/recently-played",
            headers=self.headers,
            params={"limit": 10},
        )

        return response

    def get_user_data(self):
        response = requests.get(
            self.API_URL + "/me",
            headers=self.headers,
        )

        return response

    def get_audio_features(self, uris) -> Response:
        response = requests.get(
            self.API_URL + "/audio-features",
            headers=self.headers,
            params={"ids": uris},
        )

        return response

    def search(self, search_term, search_type) -> Response:
        response = requests.get(
            self.API_URL + "/search",
            headers=self.headers,
            params={"q": search_term, "type": search_type},
        )

        return response

    def play_track(self, body) -> Response:
        response = requests.put(
            self.API_URL + "/me/player/play",
            headers=self.headers,
            json=body,
        )

        return response

    def skip_track(self) -> Response:
        response = requests.post(
            self.API_URL + "/me/player/next",
            headers=self.headers,
        )

        return response

    def pause_playback(self) -> Response:
        response = requests.put(
            self.API_URL + "/me/player/pause",
            headers=self.headers,
        )

        return response

    def add_to_queue(self, params) -> Response:
        response = requests.post(
            self.API_URL + "/me/player/queue", headers=self.headers, params=params
        )

        return response

    def get_next_track(self, params) -> Optional[str]:
        response = requests.get(
            self.API_URL + "/recommendations",
            headers=self.headers,
            params=params,
        )
        tracks = response.json()["tracks"]
        for track in tracks:
            if track["uri"] not in self.queue:
                self.queue.append(track["uri"])
                return track["uri"]

        return None

    def get_queue(self) -> dict[str, Any]:
        def _filter(element: dict[str, Any]) -> dict[str, Any]:
            return {
                "id": element["id"],
                "name": element["name"],
                "artists": [{"name": artist["name"] for artist in element["artists"]}],
                "album_name": element["album"]["name"],
                "album_image_url": element["album"]["images"][1]["url"],
                "link": element["external_urls"]["spotify"],
            }

        response = requests.get(
            self.API_URL + "/me/player/queue",
            headers=self.headers,
        )

        data = response.json()
        concatenated = [data["currently_playing"]] + data["queue"]
        seen_id = set()
        filtered = []

        for element in concatenated:
            if element["id"] not in seen_id:
                filtered.append(_filter(element))
                seen_id.add(element["id"])

        res = {
            "currently_playing": filtered[0],
            "queue": [filtered[0]] if len(filtered) == 1 else filtered[1:],
        }
        return res

    def get_df_from_tracks(self, tracks: list[dict[str, Any]]) -> pd.DataFrame:
        song_names, song_artists, ids = [], [], []
        for item in tracks:
            track = item["track"] if item.get("track") else item
            ids.append(track["id"])
            song_names.append(track["name"])
            song_artists.append([artist["name"] for artist in track["artists"]])

        uris = ",".join(ids)
        audio_features = self.get_audio_features(uris).json()["audio_features"]

        df_features = pd.DataFrame(audio_features)
        df_artists = pd.DataFrame({"artists": song_artists})
        df_song_names = pd.DataFrame({"tracks": song_names})

        return pd.concat([df_artists, df_song_names, df_features], axis=1)
