import requests
from requests import Response

LIMIT = 50


class Spotify:
    API_URL = "https://api.spotify.com/v1"

    def __init__(self, token):
        self.token = token

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

    def get_user_data(self):
        response = requests.get(
            self.API_URL + "/me",
            headers=self.headers,
        )

        return response

    def get_audio_features(self, uris) -> Response:
        response = requests.get(
            self.API_URL + "/audio-features", headers=self.headers, params={"ids": uris}
        )

        return response

    def search(self, search_term, search_type) -> Response:
        response = requests.get(
            self.API_URL + "/search",
            headers=self.headers,
            params={"q": search_term, "type": search_type},
        )

        return response
