# ZundaGPT2
#
# VOICEVOX APIクラス
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import json
import requests

from .voicevox_speaker import VoicevoxSpeaker

class VoicevoxAPI:
    DEFAULT_SERVER = "http://127.0.0.1:50021"
    server = DEFAULT_SERVER

    # バージョンを取得する
    @staticmethod
    def get_version(print_error=False) -> str:
        try:
            response = requests.get(f"{VoicevoxAPI.server}/version")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            if print_error:
                print(err)
            return None

    # 話者リストを取得する
    @staticmethod
    def get_speakers(print_error=True) -> list:
        try:
            response = requests.get(f"{VoicevoxAPI.server}/speakers")
            response.raise_for_status()
            items = response.json()
            speakers = []
            for item in items:
                styles = item["styles"]
                for style in styles:
                    speakers.append(VoicevoxSpeaker(style["id"], item["name"], style["name"]))
            return speakers
        except Exception as err:
            if print_error:
                print(err)
            return None
        
    # テキストの読み上げ用データを取得する
    @staticmethod
    def audio_query(text: str, speaker_id: int, print_error=True) -> dict:
        try:
            post_params = {"text": text, "speaker": speaker_id}
            response = requests.post(f"{VoicevoxAPI.server}/audio_query", params=post_params)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            if print_error:
                print(err)
            return None

    # 音声データを生成する
    @staticmethod
    def synthesis(query_json: dict, speaker_id: int, print_error=True) -> bytes:
        try:
            post_params = {"speaker": speaker_id}
            response = requests.post(f"{VoicevoxAPI.server}/synthesis", params=post_params, data=json.dumps(query_json))
            response.raise_for_status()
            return response.content
        except Exception as err:
            if print_error:
                print(err)
            return None

    # 音声データを生成する
    @staticmethod
    def get_wave_data(speaker_id: int, text: str, speed_scale: float=1, pitch_scale: float=0, print_error=True) -> bytes:
        query_json = VoicevoxAPI.audio_query(text, speaker_id)
        if query_json is None:
            return None
        query_json["speedScale"] = speed_scale
        query_json["pitchScale"] = pitch_scale
        wave_data = VoicevoxAPI.synthesis(query_json, speaker_id, print_error)
        return wave_data
