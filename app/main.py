# ZundaGPT2
#
# メイン
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import copy

import webview
from openai import APITimeoutError

from settings import Settings
from chat import ChatFactory
from chat import Chat
from character import CharacterVoicevox
from character import CharacterCoeiroink
from character import CharacterAIVoice
from chat_log import ChatLog

APP_NAME = "ZundaGPT2"
APP_VERSION = "0.2.0"
COPYRIGHT = "Copyright 2024 led-mirage"

# アプリケーションクラス
class Application:
    # コンストラクタ
    def __init__(self):
        self.settings = None
        self.chat = None
        self.settings = None
        self.user_character = None
        self.assistant_character = None
        self.window = None
    
    # 開始する
    def start(self):
        window_title = f"{APP_NAME}  ver {APP_VERSION}"
        self.window = webview.create_window(window_title, url="html/index.html", width=600, height=800, js_api=self, text_select=True)
        webview.start()

    # ページロードイベントハンドラ（UI）
    def page_loaded(self):
        self.new_chat()

    # 新しいチャットを開始する
    def new_chat(self):
        self.settings = Settings()
        self.settings.load()
        
        ChatLog.LOG_FOLDER = self.settings.system["log_folder"]

        self.chat = ChatFactory.create(
            self.settings.chat["api"],
            self.settings.chat["model"],
            self.settings.chat["instruction"],
            self.settings.chat["bad_response"],
            self.settings.chat["history_size"]
        )

        self.user_character = self.create_user_character()
        self.assistant_character = self.create_assistant_character()
        self.set_chatinfo_to_ui()

    # チャットの情報をUIに通知する
    def set_chatinfo_to_ui(self):
        user_name = self.settings.user["name"]
        user_color = self.settings.user["name_color"]
        assistant_name = self.settings.assistant["name"]
        assistant_color = self.settings.assistant["name_color"]
        self.window.evaluate_js(f"setChatInfo('{user_name}', '{user_color}', '{assistant_name}', '{assistant_color}')")

    # ひとつ前のチャットを表示して続ける
    def prev_chat(self):
        logfile = ChatLog.get_prev_logfile(self.chat)
        if logfile is None:
            return

        loaded_settings, loaded_chat = ChatLog.load(logfile)
        if loaded_settings is None:
            return
        
        self.change_current_chat(loaded_settings, loaded_chat)

    # ひとつ後のチャットを表示して続ける
    def next_chat(self):
        logfile = ChatLog.get_next_logfile(self.chat)
        if logfile is None:
            return

        loaded_settings, loaded_chat = ChatLog.load(logfile)
        if loaded_settings is None:
            return
        
        self.change_current_chat(loaded_settings, loaded_chat)

    # カレントチャットを変更する
    def change_current_chat(self, loaded_settings: Settings, loaded_chat: Chat):
        self.settings = loaded_settings
        self.chat = loaded_chat
        self.user_character = self.create_user_character()
        self.assistant_character = self.create_assistant_character()
        self.set_chatinfo_to_ui()
        self.set_chatmessages_to_ui(loaded_chat.messages)

    # カレントチャットを削除する
    def delete_current_chat(self):
        if not ChatLog.exists_log_file(self.chat):
            return
          
        next_logfile = ChatLog.get_prev_logfile(self.chat)
        if next_logfile is None:
            next_logfile = ChatLog.get_next_logfile(self.chat)
        if next_logfile is None:
            return
        
        ChatLog.delete_log_file(self.chat)
        
        loaded_settings, loaded_chat = ChatLog.load(next_logfile)
        if loaded_settings is None:
            return

        self.change_current_chat(loaded_settings, loaded_chat)

    # チャットの内容をUIに送信する
    def set_chatmessages_to_ui(self, messages: list[dict]):
        self.window.evaluate_js(f"setChatMessages({messages})")

    # メッセージ送信イベントハンドラ（UI）
    def send_message_to_chatgpt(self, text):
        if self.user_character is not None:
            self.user_character.talk(text)
        self.window.evaluate_js(f"startResponse()")
        self.chat.send_message(
            text,
            self.on_recieve_chunk,
            self.on_recieve_sentence,
            self.on_end_response,
            self.on_chat_timeout,
            self.on_chat_error)

    # チャンク受信イベントハンドラ（Chat）
    def on_recieve_chunk(self, chunk):
        self.window.evaluate_js(f"addChunk('{self.escape_js_string(chunk)}')")

    # センテンス読み上げイベントハンドラ（Chat）
    def on_recieve_sentence(self, sentence):
        if self.assistant_character is not None:
            self.assistant_character.talk(sentence)
        self.window.evaluate_js(f"parsedSentence('{self.escape_js_string(sentence)}')")
    
    # レスポンス受信完了イベントハンドラ（Chat）
    def on_end_response(self, response):
        ChatLog.save(self.settings, self.chat)
        self.window.evaluate_js(f"endResponse()")

    # タイムアウトイベントハンドラ（Chat）
    def on_chat_timeout(self, e: APITimeoutError):
        print(e)
        self.window.evaluate_js(f"handleChatTimeout()")

    # 例外イベントハンドラ（Chat）
    def on_chat_error(self, e: Exception):
        print(e)
        self.window.evaluate_js(f"handleChatException()")

    # 文字をエスケープする
    def escape_js_string(self, s):
        return (
            s.replace('\\', '\\\\')  # バックスラッシュを最初にエスケープ
            .replace('\n', '\\n')    # 改行
            .replace('\r', '\\r')    # キャリッジリターン
            .replace('\t', '\\t')    # タブ
            .replace('"', '\\"')     # ダブルクォーテーション
            .replace('\'', '\\\'')   # シングルクォート
        )

    # TTS用キャラクターを作成する（ユーザー）
    def create_user_character(self):
        param = copy.deepcopy(self.settings.user)
        param["tts_software_path"] = self.settings.get_user_tts_software_path()
        return self.create_character(param)

    # TTS用キャラクターを作成する（アシスタント）
    def create_assistant_character(self):
        param = copy.deepcopy(self.settings.assistant)
        param["tts_software_path"] = self.settings.get_assistant_tts_software_path()
        return self.create_character(param)

    # TTS用キャラクターを作成する（ヘルパー）
    def create_character(self, param: dict):
        tts_software = param["tts_software"]
        tts_software_path = param["tts_software_path"]
        speaker_id = param["speaker_id"]
        speed_scale = param["speed_scale"]
        pitch_scale = param["pitch_scale"]

        if tts_software == "VOICEVOX":
            return CharacterVoicevox(speaker_id, speed_scale, pitch_scale, tts_software_path)
        elif tts_software == "COEIROINK":
            return CharacterCoeiroink(speaker_id, speed_scale, pitch_scale, tts_software_path)
        elif tts_software == "AIVOICE":
            return CharacterAIVoice(speaker_id, tts_software_path)
        else:
            return None

if __name__ == '__main__':
    app = Application()
    app.start()
