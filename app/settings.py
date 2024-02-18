# ZundaGPT2
#
# メイン
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import copy
import json
import os
import threading

from voiceapi import VoicevoxAPI
from voiceapi import CoeiroinkApi
from character import CharacterVoicevox
from character import CharacterAIVoice

class Settings:
    FILE_VER = 2
    FILE_SETTINGS = "settings.json"

    def __init__(self, setting_file_path=FILE_SETTINGS):
        self._setting_file_path = setting_file_path
        self._lock = threading.Lock()
        self._init_member()

    def _init_member(self):
        self.user = {
            "name": "あなた",
            "name_color": "#007bff",
            "tts_software": "VOICEVOX",
            "speaker_id": "13",    # 青山龍星
            "speed_scale": 1.2,
            "pitch_scale": 0.0,
        }
        self.assistant = {
            "name": "ずんだ",
            "name_color": "#006400",
            "tts_software": "VOICEVOX",
            "speaker_id": "3",    # ずんだもん
            "speed_scale": 1.2,
            "pitch_scale": 0.0,
        }
        self.chat = {
            "api": "OpenAI",
            "model": "gpt-3.5-turbo-1106",
            "instruction": "君は優秀なアシスタント。ずんだもんの話し方で話す。具体的には語尾に「のだ」または「なのだ」をつけて自然に話す。回答は１００文字以内で簡潔に行う。",
            "bad_response": "答えられないのだ",
            "history_size": 6,
        }
        self.tts = {
            "voicevox_server": VoicevoxAPI.DEFAULT_SERVER,
            "voicevox_path": CharacterVoicevox.DEFAULT_INSTALL_PATH,
            "coeiroink_server": CoeiroinkApi.DEFAULT_SERVER,
            "coeiroink_path": "",
            "aivoice_path": CharacterAIVoice.DEFAULT_INSTALL_PATH,
        }
        self.system = {
            "log_folder": "log",
        }

    # deepcopy
    def __deepcopy__(self, memo):
        new_copy = self.__class__(None)
        memo[id(self)] = new_copy
        new_copy._setting_file_path = self._setting_file_path
        new_copy.user = copy.deepcopy(self.user, memo)
        new_copy.assistant = copy.deepcopy(self.assistant, memo)
        new_copy.chat = copy.deepcopy(self.chat, memo)
        new_copy.tts = copy.deepcopy(self.tts, memo)
        new_copy.system = copy.deepcopy(self.system, memo)
        return new_copy

    # TTSソフトウェアのインストールパスを取得する（ユーティリティ関数）
    def get_user_tts_software_path(self):
        tts_software = self.user["tts_software"]
        return self.get_tts_software_path(tts_software)

    def get_assistant_tts_software_path(self):
        tts_software = self.assistant["tts_software"]
        return self.get_tts_software_path(tts_software)

    def get_tts_software_path(self, tts_software):
        if tts_software == "VOICEVOX":
            return self.tts["voicevox_path"]
        elif tts_software == "COEIROINK":
            return self.tts["coeiroink_path"]
        elif tts_software == "AIVOICE":
            return self.tts["aivoice_path"]
        else:
            return ""
 
    # 設定ファイルを保存する
    def save(self):
        with self._lock:
            self._save_nolock()

    def _save_nolock(self):
        with open(self._setting_file_path, "w", encoding="utf-8") as file:
            setting = {}
            setting["file_ver"] = Settings.FILE_VER
            setting["user"] = self.user
            setting["assistant"] = self.assistant
            setting["chat"] = self.chat
            setting["tts"] = self.tts
            setting["system"] = self.system

            json.dump(setting, file, ensure_ascii=False, indent=4)

    # 設定ファイルを読み込む
    def load(self):
        if not os.path.exists(self._setting_file_path):
            self._init_member()
            self._save_nolock()
            return

        with self._lock:
            with open(self._setting_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                file_ver = data.get("file_ver", 1)
                self.update_dict(self.user, data.get("user", self.user))
                self.update_dict(self.assistant, data.get("assistant", self.assistant))
                self.update_dict(self.chat, data.get("chat", self.chat))
                self.update_dict(self.tts, data.get("tts", self.tts))
                self.update_dict(self.system, data.get("system", self.system))

        if file_ver < Settings.FILE_VER:
            self._save_nolock()

        return data

    # targetにあるキーのみをsrcからコピーする
    def update_dict(self, target: dict, src: dict):
        for key in target.keys():
            if key in src:
                target[key] = src[key]
