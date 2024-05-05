import time

import requests
from requests import Response

LIMIT = 50


class Spotify:
    API_URL = "https://api.spotify.com/v1"

    def __init__(self, token=None):
        self.token = token
        if not self.token:
            self.token = open(".spotify_cached_token").read()

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token),
        }

    def get_saved_tracks(self) -> Response:
        response = requests.get(
            self.API_URL + "/me/tracks",
            headers=self.headers,
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

    def get_recommendations(self, params) -> Response:
        response = requests.get(
            self.API_URL + "/recommendations", headers=self.headers, params=params
        )

        return response

    def add_to_queue(self, params) -> Response:
        response = requests.post(
            self.API_URL + "/me/player/queue",
            headers=self.headers,
            params=params
        )

        return response
