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

from settings import Settings
from chat import Chat

# チャットログクラス
class ChatLog:
    FILE_VER = 1

    # コンストラクタ
    def __init__(self, settings: Settings):
        self.settings = settings
        pass

    # ログをファイルに保存する
    def save(self, chat: Chat):
        log_folder = self.settings.chat["log_folder"]
        if log_folder == "":
            return

        if not os.path.exists(log_folder):
            os.mkdir(log_folder)

        data = {}
        data["file_ver"] = ChatLog.FILE_VER
        data["logid"] = chat.chat_start_time.strftime("%Y%m%d%H%M%S")
        data["user"] = copy.deepcopy(self.settings.user)
        data["assistant"] = copy.deepcopy(self.settings.assistant)
        data["chat"] = copy.deepcopy(self.settings.chat)
        data["messages"] = chat.messages

        filename = self.get_logfile_name(chat)
        path = os.path.join(log_folder, filename)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    # ログファイルの名前を取得する
    def get_logfile_name(self, chat: Chat):
        return chat.chat_start_time.strftime("chatlog-%Y%m%d-%H%M%S.json")
