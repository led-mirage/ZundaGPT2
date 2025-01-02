# ZundaGPT2
#
# メイン
#
# Copyright (c) 2024-2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import sys
import copy

import webview

from app_config import AppConfig
from app_settings import Settings
from chat import ChatFactory
from chat import Chat
from character import CharacterVoicevox
from character import CharacterCoeiroink
from character import CharacterAIVoice
from character import CharacterGoogleTTS
from character import CharacterSAPI5
from chat_log import ChatLog
from voiceapi import VoicevoxAPI
from voiceapi import CoeiroinkApi

if getattr(sys, "frozen", False):
    import pyi_splash # type: ignore

APP_NAME = "ZundaGPT2"
APP_VERSION = "1.4.3-dev"
COPYRIGHT = "Copyright 2024-2025 led-mirage"

# アプリケーションクラス
class Application:
    # コンストラクタ
    def __init__(self):
        self.app_config = None
        self.settings = None
        self.chat = None
        self.settings = None
        self.user_character = None
        self.assistant_character = None
        self.last_send_message = None
        self._window = None # 先頭にアンダーバーをつけないと pywebview 5.0.x ではエラーになる
    
    # 開始する
    def start(self):
        self.app_config = AppConfig()
        self.app_config.load()
        VoicevoxAPI.server = self.app_config.tts["voicevox_server"]
        CoeiroinkApi.server = self.app_config.tts["coeiroink_server"]
        width = self.app_config.system["window_width"]
        height = self.app_config.system["window_height"]

        window_title = f"{APP_NAME}  ver {APP_VERSION}"
        self._window = webview.create_window(window_title, url="html/index.html", width=width, height=height, js_api=self, text_select=True)
        webview.start()
        #webview.start(debug=True) # 開発者ツールを表示する場合

    # ページロードイベントハンドラ（UI）
    def page_loaded(self):
        if self.chat == None:
            self.new_chat()
        else:
            self.set_chatinfo_to_ui()
            self.set_chatmessages_to_ui(self.chat.messages)
            self.set_window_title()

    # 新しいチャットを開始する
    def new_chat(self):
        self.settings = Settings()
        self.settings.load()
        
        ChatLog.LOG_FOLDER = self.app_config.system["log_folder"]

        self.chat = ChatFactory.create(
            self.settings.chat["api"],
            self.settings.chat["model"],
            self.settings.chat["instruction"],
            self.settings.chat["bad_response"],
            self.settings.chat["history_size"],
            self.app_config.system["chat_api_timeout"],
            self.app_config.gemini
        )

        self.user_character = self.create_user_character()
        self.assistant_character = self.create_assistant_character()
        self.set_chatinfo_to_ui()
        self.set_window_title()

    # ウィンドウのタイトルを設定する
    def set_window_title(self):
        logfile = ChatLog.get_logfile_name(self.chat)
        window_title = f"{APP_NAME}  ver {APP_VERSION} - {logfile}"
        self._window.set_title(window_title)

    # チャットの情報をUIに通知する
    def set_chatinfo_to_ui(self):
        display_name = self.settings.settings.get("display_name", "")
        user_name = self.settings.user["name"]
        user_color = self.settings.user["name_color"]
        assistant_name = self.settings.assistant["name"]
        assistant_color = self.settings.assistant["name_color"]
        speaker_on = self.app_config.system["speaker_on"]
        welcome_title = self.settings.settings.get("welcome_title", "")
        welcome_message = self.settings.settings.get("welcome_message", "")
        self._window.evaluate_js(
            f"setChatInfo('{display_name}', '{user_name}', '{user_color}', '{assistant_name}', '{assistant_color}', {str(speaker_on).lower()}, '{welcome_title}', '{welcome_message}')")

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
        self.set_window_title()

    # チャットの内容をUIに送信する
    def set_chatmessages_to_ui(self, messages: list[dict]):
        self._window.evaluate_js(f"setChatMessages({messages})")

    # コピーライト取得
    def get_copyright(self):
        return COPYRIGHT

    # カレントチャット削除イベントハンドラ（UI）
    def delete_current_chat(self):
        if not ChatLog.exists_log_file(self.chat):
            return
          
        next_logfile = ChatLog.get_prev_logfile(self.chat)
        if next_logfile is None:
            next_logfile = ChatLog.get_next_logfile(self.chat)
        
        ChatLog.delete_log_file(self.chat)
        
        if next_logfile is not None:
            loaded_settings, loaded_chat = ChatLog.load(next_logfile)
            if loaded_settings is None:
                return

            self.change_current_chat(loaded_settings, loaded_chat)
        else:
            self._window.evaluate_js(f"newChat()")

    # 設定画面遷移イベントハンドラ（UI）
    def move_to_settings(self):
        self._window.load_url("html/settings.html")

    # 設定画面ファイル一覧要求イベントハンドラ（UI）
    def get_settings_files(self):
        settings_files = Settings.get_settings_files()

        current_settings_file = self.app_config.system["settings_file"]

        view_model = []
        for filename in settings_files:
            settings = Settings(filename)
            settings.load()
            current = filename == current_settings_file
            diaplayName = settings.settings["display_name"]
            description = settings.settings["description"]
            view_model.append({
                "current": current,
                "filename": filename,
                "displayName": diaplayName,
                "description": description,
                "userName": settings.user["name"],
                "assistantName": settings.assistant["name"],
                "api": settings.chat["api"],
                "model": settings.chat["model"]
            })
        return view_model

    # 設定画面確定イベントハンドラ（UI）
    def submit_settings(self, settings_file):
        self._window.load_url("html/index.html")
        self.app_config.system["settings_file"] = settings_file
        self.app_config.save()
        self.chat = None

    # 設定画面キャンセルイベントハンドラ（UI）
    def cancel_settings(self):
        self._window.load_url("html/index.html")

    # メッセージ送信イベントハンドラ（UI）
    def send_message_to_chatgpt(self, text, speak=True):
        if self.user_character is not None and self.app_config.system["speaker_on"] and speak:
            self.user_character.talk(text)
        self._window.evaluate_js(f"startResponse()")
        self.last_send_message = text
        self.chat.send_message(
            text,
            self.on_recieve_chunk,
            self.on_recieve_sentence,
            self.on_end_response,
            self.on_chat_error)

    # メッセージ再送信イベントハンドラ（UI）
    def retry_send_message_to_chatgpt(self):
        self.chat.send_message(
            self.last_send_message,
            self.on_recieve_chunk,
            self.on_recieve_sentence,
            self.on_end_response,
            self.on_chat_error)
        
    # メッセージ送信中止イベントハンドラ（UI）
    def stop_send_message_to_chatgpt(self):
        self.chat.stop_send_message()
    
    # スピーカーのON/OFFを切り替えるイベントハンドラ（UI）
    def toggle_speaker(self):
        self.app_config.system["speaker_on"] = not self.app_config.system["speaker_on"]
        self.app_config.save()

    # メッセージ削除イベントハンドラ（UI）
    def trancate_messages(self, index):
        self.chat.truncate_messages(index)
        ChatLog.save(self.settings, self.chat)

    # 別の回答を取得するイベントハンドラ（UI）
    def ask_another_reply_to_chatgpt(self, index):
        text = self.chat.messages[index - 1]["content"]
        self.chat.truncate_messages(index - 1)
        ChatLog.save(self.settings, self.chat)
        self.send_message_to_chatgpt(text, speak=False)

    # チャンク受信イベントハンドラ（Chat）
    def on_recieve_chunk(self, chunk):
        self._window.evaluate_js(f"addChunk('{self.escape_js_string(chunk)}')")

    # センテンス読み上げイベントハンドラ（Chat）
    def on_recieve_sentence(self, sentence):
        if self.assistant_character is not None and self.app_config.system["speaker_on"]:
            self.assistant_character.talk(sentence)
        self._window.evaluate_js(f"parsedSentence('{self.escape_js_string(sentence)}')")
    
    # レスポンス受信完了イベントハンドラ（Chat）
    def on_end_response(self, content):
        ChatLog.save(self.settings, self.chat)
        self._window.evaluate_js(f"endResponse('{self.escape_js_string(content)}')")

    # チャット例外イベントハンドラ（Chat）
    def on_chat_error(self, e: Exception, cause: str, info: str=""):
        module_name = type(e).__module__
        class_name = type(e).__name__
        print(f"{module_name}.{class_name}")
        print(e)

        if cause == "Timeout":
            message = "APIの呼び出しがタイムアウトしたのだ"
            self._window.evaluate_js(f"handleChatTimeoutException('{message}')")
        else:
            if cause == "Authentication":
                message = "APIの認証に失敗したのだ"
            elif cause == "EndPointNotFound":
                message = "APIのエンドポイントが間違っているのだ"
            elif cause == "UnsafeContent":
                message = "会話の内容が不適切だと判断されたのだ"
            elif cause == "RateLimit":
                message = "レート制限に達したのだ"
            elif cause == "APIError":
                message = f"APIエラーが発生したのだ\n{info}"
            else:
                message = f"なんかわからないエラーが発生したのだ（{class_name}）"
            self._window.evaluate_js(f"handleChatException('{message}')")

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
        return self.create_character(param)

    # TTS用キャラクターを作成する（アシスタント）
    def create_assistant_character(self):
        param = copy.deepcopy(self.settings.assistant)
        return self.create_character(param)

    # TTS用キャラクターを作成する（ヘルパー）
    def create_character(self, param: dict):
        tts_software = param["tts_software"]
        tts_software_path = self.app_config.get_tts_software_path(tts_software)
        speaker_id = param["speaker_id"]
        speed_scale = param["speed_scale"]
        pitch_scale = param["pitch_scale"]

        character = None
        if tts_software == "VOICEVOX":
            character = CharacterVoicevox(speaker_id, speed_scale, pitch_scale, tts_software_path)
        elif tts_software == "COEIROINK":
            character = CharacterCoeiroink(speaker_id, speed_scale, pitch_scale, tts_software_path)
        elif tts_software == "AIVOICE":
            character = CharacterAIVoice(speaker_id, tts_software_path)
        elif tts_software == "GTTS":
            character = CharacterGoogleTTS()
        elif tts_software == "SAPI5":
            character = CharacterSAPI5(speaker_id, speed_scale)
        else:
            character = None

        if character is not None:
            if hasattr(character, "is_available"):
                (available, message) = character.is_available()
                if not available:
                    message = message.replace("\n", "\\n")
                    self._window.evaluate_js(f"handleChatException('{message}')")
                    character = None

        return character

    # チャットのリプレイ
    def replay(self):
        def process_sentence(sentence):
            self._window.evaluate_js(f"addReplayMessage('{self.escape_js_string(sentence)}')")

            if message["role"] == "assistant":
                self.assistant_character.talk(sentence)
            else:
                self.user_character.talk(sentence)

        for message in self.chat.messages:
            self._window.evaluate_js(f"startReplayMessageBlock('{self.escape_js_string(message["role"])}')")
            sentence = ""
            for c in message["content"]:
                sentence += c
                if sentence.endswith(("。", "\n", "？", "！")):
                    process_sentence(sentence)
                    sentence = ""
            
            if sentence != "":
                process_sentence(sentence)

            self._window.evaluate_js(f"endReplayMessageBlock('{self.escape_js_string(message["content"])}')")

        self._window.evaluate_js(f"setChatMessages({self.chat.messages})")

if __name__ == '__main__':
    if getattr(sys, "frozen", False):
        pyi_splash.close()

    app = Application()
    app.start()
