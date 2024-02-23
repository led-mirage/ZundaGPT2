# ZundaGPT2
#
# COEIROINK APIクラス
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import json

import requests

class CoeiroinkApi:
    DEFAULT_SERVER = "http://127.0.0.1:50032"
    server = DEFAULT_SERVER

    # ステータスを取得する
    @staticmethod
    def get_status(print_error=False) -> str:
        try:
            response = requests.get(f"{CoeiroinkApi.server}/")
            response.raise_for_status()
            return response.json()["status"]
        except Exception as err:
            if print_error:
                print(err)
            return None

    # 話者リストを取得する
    @staticmethod
    def get_speakers(print_error=True) -> dict:
        try:
            response = requests.get(f"{CoeiroinkApi.server}/v1/speakers")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            if print_error:
                print(err)
            return None

    # スタイルIDから話者情報を取得する
    @staticmethod
    def get_speaker_info(styleId: int, print_error=True) -> dict:
        try:
            post_params = {"styleId": styleId}
            response = requests.post(f"{CoeiroinkApi.server}/v1/style_id_to_speaker_meta", params=post_params)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            if print_error:
                print(err)
            return None

    # テキストの読み上げ用データを取得する
    @staticmethod
    def estimate_prosody(text: str, print_error=True) -> dict:
        try:
            post_params = {"text": text}
            response = requests.post(f"{CoeiroinkApi.server}/v1/estimate_prosody", data=json.dumps(post_params))
            response.raise_for_status()
            return response.json()
        except Exception as err:
            if print_error:
                print(err)
            return None

    # 音声データを生成する
    @staticmethod
    def synthesis(speaker: dict, text: str, prosody: dict,
                  speedScale = 1, volumeScale = 1, pitchScale = 0, intonationScale = 1,
                  prePhonemeLength = 0.1, postPhonemeLength = 0.1, outputSamplingRate = 24000, print_error=True) -> bytes:
        post_params = {
            "speakerUuid": speaker["speakerUuid"],
            "styleId": speaker["styleId"],
            "text": text,
            "prosodyDetail": prosody["detail"],
            "speedScale": speedScale,
            "volumeScale": volumeScale,
            "pitchScale": pitchScale,
            "intonationScale": intonationScale,
            "prePhonemeLength": prePhonemeLength,
            "postPhonemeLength": postPhonemeLength,
            "outputSamplingRate": outputSamplingRate
        }
        try:
            response = requests.post(f"{CoeiroinkApi.server}/v1/synthesis", data=json.dumps(post_params))
            response.raise_for_status()
            return response.content
        except Exception as err:
            if print_error:
                print(err)
                print(f"error text: {text}")
            return None

    # 音声データを生成する
    @staticmethod
    def get_wave_data(styleId: int, text: str,
                      speedScale = 1, volumeScale = 1, pitchScale = 0, intonationScale = 1,
                      prePhonemeLength = 0.1, postPhonemeLength = 0.1, outputSamplingRate = 24000, print_error=True) -> bytes:

        speaker = CoeiroinkApi.get_speaker_info(styleId)
        if speaker is None:
            return None
        
        prosody = CoeiroinkApi.estimate_prosody(text)
        if prosody is None:
            return None

        return CoeiroinkApi.synthesis(speaker, text, prosody,
                                      speedScale, volumeScale, pitchScale, intonationScale,
                                      prePhonemeLength, postPhonemeLength, outputSamplingRate, print_error)
