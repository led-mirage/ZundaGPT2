# ZundaGPT2
#
# チャット設定クラス
#
# Copyright (c) 2024-2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import copy
import json
import os
import glob
import threading

from config.app_config import AppConfig

class Settings:
    FILE_VER = 8
    FOLDER_NAME = "settings"

    def __init__(self, settings_filename=None):
        if settings_filename is None:
            app_config = AppConfig()
            app_config.load()
            settings_filename = app_config.system["settings_file"]

        if not os.path.exists(Settings.FOLDER_NAME):
            os.makedirs(Settings.FOLDER_NAME)
        self._settings_file_path = os.path.join(Settings.FOLDER_NAME, settings_filename)
        self._lock = threading.Lock()
        self._init_member()

    def _init_member(self):
        self.settings = {
            "display_name": "ZundaGPT",
            "description": "既定値",
            "welcome_title": "Welcome",
            "welcome_message": "なんでも聞いてほしいのだ！",
            "group": "Default"
        }
        self.user = {
            "name": "あなた",
            "name_color": "#007bff",
            "icon": "",
            "tts_software": "VOICEVOX",
            "speaker_id": "13",    # 青山龍星
            "speed_scale": 1.2,
            "pitch_scale": 0.0,
        }
        self.assistant = {
            "name": "ずんだ",
            "name_color": "#006400",
            "icon": "",
            "tts_software": "VOICEVOX",
            "speaker_id": "3",    # ずんだもん
            "speed_scale": 1.2,
            "pitch_scale": 0.0,
        }
        self.chat = {
            "api": "OpenAI",
            "api_key_envvar": "",
            "api_endpoint_envvar": "",
            "model": "gpt-3.5-turbo-0125",
            "instruction": "君は優秀なアシスタント。ずんだもんの話し方で話す。具体的には語尾に「のだ」または「なのだ」をつけて自然に話す。回答は１００文字以内で簡潔に行う。",
            "bad_response": "答えられないのだ",
            "history_size": 6,
        }
        self.claude_options = {
            "max_tokens": 4096,
            "extended_thinking": False,
            "budget_tokens": 2048,
        }

    # deepcopy
    def __deepcopy__(self, memo):
        new_copy = self.__class__(None)
        memo[id(self)] = new_copy
        new_copy._settings_file_path = self._settings_file_path
        new_copy.settings = copy.deepcopy(self.settings, memo)
        new_copy.user = copy.deepcopy(self.user, memo)
        new_copy.assistant = copy.deepcopy(self.assistant, memo)
        new_copy.chat = copy.deepcopy(self.chat, memo)
        new_copy.claude_options = copy.deepcopy(self.claude_options, memo)
        return new_copy

    # 設定ファイルを保存する
    def save(self):
        with self._lock:
            self._save_nolock()

    def _save_nolock(self):
        with open(self._settings_file_path, "w", encoding="utf-8") as file:
            setting = {}
            setting["file_ver"] = Settings.FILE_VER
            setting["settings"] = self.settings
            setting["user"] = self.user
            setting["assistant"] = self.assistant
            setting["chat"] = self.chat
            setting["claude_options"] = self.claude_options

            json.dump(setting, file, ensure_ascii=False, indent=4)

    # 設定ファイルを読み込む
    def load(self):
        if not os.path.exists(self._settings_file_path):
            self._init_member()
            self._save_nolock()
            return

        with self._lock:
            with open(self._settings_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                file_ver = data.get("file_ver", 1)
                self.update_dict(self.settings, data.get("settings", self.settings))
                self.update_dict(self.user, data.get("user", self.user))
                self.update_dict(self.assistant, data.get("assistant", self.assistant))
                self.update_dict(self.chat, data.get("chat", self.chat))
                self.update_dict(self.claude_options, data.get("claude_options", self.claude_options))

        if file_ver < Settings.FILE_VER:
            self._save_nolock()

        return data

    # targetにあるキーのみをsrcからコピーする
    def update_dict(self, target: dict, src: dict):
        for key in target.keys():
            if key in src:
                target[key] = src[key]

    # 設定ファイルのパスを取得する
    def get_path(self):
        return self._settings_file_path

    @classmethod
    def get_settings_files(cls):
        json_paths = glob.glob(cls.FOLDER_NAME + "/*.json")

        json_files = []
        for file_path in json_paths:
            file_name = os.path.basename(file_path)
            json_files.append(file_name)
        return json_files
