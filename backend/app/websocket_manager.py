import asyncio
import datetime
import random
from typing import Any, Callable

import numpy as np
import pandas as pd
from fastapi import WebSocket, WebSocketDisconnect

from models.datamodels import ClientData
from spotify.spotify import Spotify
from utils.consts import ANALYSIS_SEGMENT_LENGTH
from utils.logger import get_logger

receive_logger = get_logger(f"receive_{__name__}")
send_logger = get_logger(f"send_{__name__}")


class BaseWebSocketManager:
    def __init__(
        self,
        client_data: ClientData,
        websocket: WebSocket,
        send_stream_func: Callable[[dict], Any],
        should_start_stream_func: Callable[[], bool],
    ):
        self.client_data = client_data.model_dump()
        self.websocket = websocket
        self.send_stream_func = send_stream_func
        self.should_start_stream_func = should_start_stream_func

    async def receive_data(self) -> None:
        while True:
            try:
                data = await self.websocket.receive_json()
                receive_logger.debug(f"Receiving {data=}")
                self.client_data.update(data)
            except WebSocketDisconnect:
                receive_logger.debug("WebSocket disconnected")
                break
            except Exception as e:
                import traceback

                traceback_str = "".join(traceback.format_tb(e.__traceback__))
                send_logger.debug(f"Error: {e}, {traceback_str}")
                break

    async def send_data(self) -> None:
        while True:
            try:
                if self.should_start_stream_func():
                    send_logger.debug("Sending data...")
                    await self.send_stream_func(self.client_data)
                await asyncio.sleep(1)
            except WebSocketDisconnect:
                send_logger.debug("WebSocket disconnected")
                break
            except Exception as e:
                import traceback

                traceback_str = "".join(traceback.format_tb(e.__traceback__))
                send_logger.debug(f"Error: {e}, {traceback_str}")
                break


class WebsocketManager(BaseWebSocketManager):
    def __init__(self, websocket: WebSocket):
        super().__init__(
            client_data=ClientData(
                stopPlayback=False,
                accessToken=None,
                tempo=None,
                checked=[],
            ),
            websocket=websocket,
            send_stream_func=self.send_streaming_data,
            should_start_stream_func=(
                lambda: self.client_data["accessToken"] is not None
            ),
        )

    def get_feedback_df(
        self, feedback_type: list[str], tracks_df: pd.DataFrame
    ) -> tuple[pd.DataFrame, Callable]:
        if feedback_type == ["Calm & Relaxing"]:
            tracks_df["danceability_var"] = (0.4 - tracks_df["danceability"]) ** 2
            tracks_df["energy_var"] = (0.4 - tracks_df["energy"]) ** 2
            tracks_df["speechiness_var"] = (0.7 - tracks_df["speechiness"]) ** 2
            tracks_df["acousticness_var"] = (0.7 - tracks_df["acousticness"]) ** 2
            tracks_df["instrumentalness_var"] = (0.5 - tracks_df["instrumentalness"]) ** 2
            tracks_df["liveness_var"] = (0.8 - tracks_df["liveness"]) ** 2
            tracks_df["valence_var"] = (0.8 - tracks_df["valence"]) ** 2

            def affected(df: pd.DataFrame) -> bool:
                value = np.percentile(df["alpha"], 75) - np.percentile(df["alpha"], 25)
                return value > 0

        elif feedback_type == ["High-Energy & Adventurous"]:
            tracks_df["danceability_var"] = (0.7 - tracks_df["danceability"]) ** 2
            tracks_df["energy_var"] = (0.7 - tracks_df["energy"]) ** 2
            tracks_df["speechiness_var"] = (0.4 - tracks_df["speechiness"]) ** 2
            tracks_df["acousticness_var"] = (0.4 - tracks_df["acousticness"]) ** 2
            tracks_df["instrumentalness_var"] = (0.4 - tracks_df["instrumentalness"]) ** 2
            tracks_df["liveness_var"] = (0.5 - tracks_df["liveness"]) ** 2
            tracks_df["valence_var"] = (0.8 - tracks_df["valence"]) ** 2

            # TODO: Is this supposed to be (beta - alpha) instead of (beta - beta)?
            def affected(df: pd.DataFrame) -> bool:
                value = np.percentile(df["beta"], 75) - np.percentile(df["alpha"], 25)
                return value > 0

        elif feedback_type == ["Self-Exploration & Intellectual"]:
            tracks_df["danceability_var"] = (0.5 - tracks_df["danceability"]) ** 2
            tracks_df["energy_var"] = (0.5 - tracks_df["energy"]) ** 2
            tracks_df["speechiness_var"] = (0.6 - tracks_df["speechiness"]) ** 2
            tracks_df["acousticness_var"] = (0.7 - tracks_df["acousticness"]) ** 2
            tracks_df["instrumentalness_var"] = (0.7 - tracks_df["instrumentalness"]) ** 2
            tracks_df["liveness_var"] = (0.5 - tracks_df["liveness"]) ** 2
            tracks_df["valence_var"] = (0.9 - tracks_df["valence"]) ** 2

            def affected(df: pd.DataFrame) -> bool:
                value = np.percentile(df["theta"], 75) - np.percentile(df["theta"], 25)
                return value > 0

        # TODO: not implemented yet
        elif feedback_type == "High-Octane & Relaxing":
            tracks_df["danceability_var"] = (0.7 - tracks_df["danceability"]) ** 2
            tracks_df["energy_var"] = (0.7 - tracks_df["energy"]) ** 2
            tracks_df["speechiness_var"] = (0.7 - tracks_df["speechiness"]) ** 2
            tracks_df["acousticness_var"] = (0.7 - tracks_df["acousticness"]) ** 2
            tracks_df["instrumentalness_var"] = (0.7 - tracks_df["instrumentalness"]) ** 2
            tracks_df["liveness_var"] = (0.7 - tracks_df["liveness"]) ** 2
            tracks_df["valence_var"] = (0.8 - tracks_df["valence"]) ** 2

            def affected(df: pd.DataFrame) -> bool:
                raise NotImplementedError(str(df))

        else:
            raise Exception("unmatched feedback type")

        tracks_df = tracks_df.sort_values(
            [
                "danceability_var",
                "energy_var",
                "speechiness_var",
                "acousticness_var",
                "instrumentalness_var",
                "liveness_var",
                "valence_var",
            ],
            ascending=[True, True, True, True, True, True, True],
        )

        return tracks_df, affected

    async def send_audio_feature_data(self, df: pd.DataFrame) -> None:
        data = (
            df[
                [
                    "danceability",
                    "energy",
                    "speechiness",
                    "acousticness",
                    "instrumentalness",
                    "liveness",
                    "valence",
                    "tempo",
                ]
            ]
            .mean()
            .round(2)
            .to_dict()
        )
        tempo = data.pop("tempo")

        await self.websocket.send_json(
            {
                "type": "audioFeatures",
                "data": {
                    "radarChart": data,
                    "tempo": tempo,
                },
            }
        )

    async def send_queue_data(self, data: dict[str, Any]) -> None:
        await self.websocket.send_json(
            {
                "type": "queueData",
                "data": data,
            }
        )

    async def send_brain_data(self, alpha: float, beta: float, theta: float) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ")

        await self.websocket.send_json(
            {
                "type": "brainStream",
                "data": {
                    "timestamp": timestamp,
                    "data": {"alpha": alpha, "beta": beta, "theta": theta},
                },
            },
        )

    async def send_streaming_data(self, client_data: dict[str, Any]) -> None:
        async def task():
            df_eeg = pd.DataFrame(columns=["alpha", "beta", "theta"])
            spotify = Spotify(client_data["accessToken"])

            # Initial queue
            recent_tracks = spotify.get_saved_tracks().json()["items"]
            df = spotify.get_df_from_tracks(recent_tracks)
            df, affected = self.get_feedback_df(client_data["checked"], df)

            # recommendation based on next track in queue
            if client_data["tempo"] is not None:
                top_matches = df.head(3)
                top_match = top_matches.iloc[
                    (top_matches["tempo"] - client_data["tempo"]).abs().argsort()[:1]
                ].iloc[0]
            else:
                top_match = df.iloc[0]

            uris = f"spotify:track:{top_match['id']}"
            spotify.play_track({"uris": [uris]})
            await asyncio.sleep(random.uniform(1, 3))
            await self.send_queue_data(spotify.get_queue())
            await self.send_audio_feature_data(df)

            while True:
                if client_data["stopPlayback"] is not None:
                    if client_data["stopPlayback"]:
                        spotify.pause_playback()
                    else:
                        spotify.play_track(None)

                    client_data["stopPlayback"] = None

                # TODO: Replace random value with actual value
                alpha = random.uniform(0.61, 1.0)
                beta = random.uniform(0.58, 0.68)
                theta = random.uniform(1.2, 2.0)

                # Send data to frontend
                await self.send_brain_data(alpha, beta, theta)

                # Process data
                df_eeg = pd.concat(
                    [
                        None if df_eeg.empty else df_eeg,
                        pd.DataFrame([{"alpha": alpha, "beta": beta, "theta": theta}]),
                    ],
                    ignore_index=True,
                )

                if len(df_eeg) % ANALYSIS_SEGMENT_LENGTH == 0:
                    if affected(df_eeg):
                        top_match = df.iloc[0]
                        recommendation_params = {
                            "seed_tracks": top_match["id"],
                            "limit": 50,
                        }
                        if client_data["tempo"]:
                            recommendation_params["target_tempo"] = client_data["tempo"]

                        next_track_uri = spotify.get_next_track(recommendation_params)
                        if next_track_uri:
                            spotify.add_to_queue({"uri": next_track_uri})
                    else:
                        # Get next track in queue
                        spotify.skip_track()

                    queue = spotify.get_queue()
                    await self.send_queue_data(queue)

                    df = spotify.get_df_from_tracks(queue["queue"])
                    df, affected = self.get_feedback_df(client_data["checked"], df)
                    await self.send_audio_feature_data(df)

                    # TODO: Reset df immediately after analysis?
                    df_eeg = pd.DataFrame(columns=["alpha", "beta", "theta"])

                await asyncio.sleep(random.uniform(1, 3))

        await asyncio.create_task(task())
