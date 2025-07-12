# ZundaGPT2
#
# メイン画面のサービス
#
# Copyright (c) 2024-2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import base64
import copy
import re

import langdetect

from config.app_config import AppConfig, get_log_settings
from config.app_settings import Settings
from app_logger import AppLogger
from app_state import AppState
from app_window import AppWindow
from chat_log import ChatLog
from const import APP_NAME, APP_VERSION
from utility.utils import get_location, get_exception_name
from utility.multi_lang import set_current_language, get_text_resource
from chat.chat import ChatFactory, Chat
from character import (
    CharacterAIVoice,
    CharacterCoeiroink,
    CharacterGoogleTTS,
    CharacterSAPI5,
    CharacterVoicevox
)


log_settings = get_log_settings()
AppLogger.init_logger(log_settings["log_folder"], log_settings["log_level"])


class IndexService:
    def __init__(self, app_config: AppConfig, state: AppState, window: AppWindow):
        self.app_config = app_config
        self.state = state
        self.window = window

    # ページロードイベントハンドラ（UI）
    def page_loaded(self):
        lang = self.app_config.system["language"]
        set_current_language(lang)

        if self.state.chat == None:
            self.new_chat()
        else:
            self.set_chatinfo_to_ui()
            self.set_chatmessages_to_ui(self.state.chat.messages)
            self.set_window_title()
            if self.state.initial_message_index >= 0:
                self.window.js.moveToMessageAt(self.state.initial_message_index, self.state.initial_highlight_text)
                self.state.initial_message_index = -1
                self.state.initial_highlight_text = ""

    # 新しいチャットを開始する
    def new_chat(self):
        self.state.settings = Settings()
        self.state.settings.load()
        
        ChatLog.LOG_FOLDER = self.app_config.system["log_folder"]

        self.state.chat = ChatFactory.create(
            self.state.settings.chat["api"],
            self.state.settings.chat["model"],
            self.state.settings.chat["instruction"],
            self.state.settings.chat["bad_response"],
            self.state.settings.chat["history_size"],
            self.state.settings.chat["history_char_limit"],
            self.app_config.system["chat_api_timeout"],
            self.state.settings.chat["api_key_envvar"],
            self.state.settings.chat["api_endpoint_envvar"],
            self.app_config.gemini,
            self.state.settings.claude_options
        )

        self.state.user_character = self.create_user_character()
        self.state.assistant_character = self.create_assistant_character()
        self.set_chatinfo_to_ui()
        self.set_window_title()

    # ウィンドウのタイトルを設定する
    def set_window_title(self):
        logfile = ChatLog.get_logfile_name(self.state.chat)
        window_title = f"{APP_NAME}  ver {APP_VERSION} - {logfile}"
        self.window.set_window_title(window_title)

    # 画像をBase64エンコードする
    def get_image_base64(self, path: str):
        if not path:
            return ""
        try:
            with open(path, 'rb') as f:
                data = base64.b64encode(f.read())
                return data.decode('utf-8')
        except:
            return ""

    # チャットの情報をUIに通知する
    def set_chatinfo_to_ui(self):
        display_name = self.state.settings.settings.get("display_name", "")
        user_name = self.state.settings.user["name"]
        user_color = self.state.settings.user["name_color"]
        user_icon = self.get_image_base64(self.state.settings.user["icon"])
        assistant_name = self.state.settings.assistant["name"]
        assistant_color = self.state.settings.assistant["name_color"]
        assistant_icon = self.get_image_base64(self.state.settings.assistant["icon"])
        speaker_on = self.app_config.system["speaker_on"]
        welcome_title = self.state.settings.settings.get("welcome_title", "")
        welcome_message = self.state.settings.settings.get("welcome_message", "")
        ai_agent_available = "true" if self.state.chat.is_ai_agent_available() else "false"
        ai_agent_creation_error = self.state.chat.client_creation_error

        self.window.js.setChatInfo(display_name, user_name, user_color, user_icon,
                                   assistant_name, assistant_color, assistant_icon, speaker_on,
                                   welcome_title, welcome_message,ai_agent_available, ai_agent_creation_error)

    # ひとつ前のチャットを表示して続ける
    def prev_chat(self):
        logfile = ChatLog.get_prev_logfile(self.state.chat)
        if logfile is None:
            return

        loaded_settings, loaded_chat = ChatLog.load(logfile)
        if loaded_settings is None:
            return
        
        self.change_current_chat(loaded_settings, loaded_chat)

    # ひとつ後のチャットを表示して続ける
    def next_chat(self):
        logfile = ChatLog.get_next_logfile(self.state.chat)
        if logfile is None:
            return

        loaded_settings, loaded_chat = ChatLog.load(logfile)
        if loaded_settings is None:
            return
        
        self.change_current_chat(loaded_settings, loaded_chat)

    # カレントチャットを変更する
    def change_current_chat(self, loaded_settings: Settings, loaded_chat: Chat):
        self.state.settings = loaded_settings
        self.state.chat = loaded_chat
        self.state.user_character = self.create_user_character()
        self.state.assistant_character = self.create_assistant_character()
        self.set_chatinfo_to_ui()
        self.set_chatmessages_to_ui(loaded_chat.messages)
        self.set_window_title()

    # チャットの内容をUIに送信する
    def set_chatmessages_to_ui(self, messages: list[dict]):
        self.window.js.setChatMessages(messages)

    # カレントチャット削除イベントハンドラ（UI）
    def delete_current_chat(self):
        if not ChatLog.exists_log_file(self.state.chat):
            return
          
        next_logfile = ChatLog.get_prev_logfile(self.state.chat)
        if next_logfile is None:
            next_logfile = ChatLog.get_next_logfile(self.state.chat)
        
        ChatLog.delete_log_file(self.state.chat)
        
        if next_logfile is not None:
            loaded_settings, loaded_chat = ChatLog.load(next_logfile)
            if loaded_settings is None:
                return

            self.change_current_chat(loaded_settings, loaded_chat)
        else:
            self.window.js.newChat()

    # メッセージ送信イベントハンドラ（UI）
    def send_message_to_chatgpt(self, text, speak=True):
        if self.state.user_character is not None and self.app_config.system["speaker_on"] and speak:
            self.state.user_character.talk(text)
        self.window.js.startResponse()
        self.state.last_send_message = text
        self.state.chat.send_message(
            text,
            self.on_recieve_chunk,
            self.on_recieve_sentence,
            self.on_recieve_paragraph,
            self.on_end_response,
            self.on_chat_error)

    # メッセージ再送信イベントハンドラ（UI）
    def retry_send_message_to_chatgpt(self):
        self.state.chat.send_message(
            self.state.last_send_message,
            self.on_recieve_chunk,
            self.on_recieve_sentence,
            self.on_recieve_paragraph,
            self.on_end_response,
            self.on_chat_error)

    # メッセージ送信中止イベントハンドラ（UI）
    def stop_send_message_to_chatgpt(self):
        self.state.chat.stop_send_message()

    # メッセージ削除イベントハンドラ（UI）
    def truncate_messages(self, index):
        self.state.chat.truncate_messages(index)
        ChatLog.save(self.state.settings, self.state.chat)

    # 別の回答を取得するイベントハンドラ（UI）
    def ask_another_reply_to_chatgpt(self, index):
        text = self.state.chat.messages[index - 1]["content"]
        self.state.chat.truncate_messages(index - 1)
        ChatLog.save(self.state.settings, self.state.chat)
        self.send_message_to_chatgpt(text, speak=False)

    # チャットメッセージのテキストを取得する（UI）
    def get_message_text(self, index):
        text = self.state.chat.messages[index]["content"] + "\n"
        return text

    # チャットのすべてのメッセージを取得する（UI）
    def get_all_message_text(self, add_header=True):
        text = ""

        if add_header:
            text += "---\n"
            text += f"{self.state.settings.settings['display_name']}\n"
            text += f"チャット開始日時: {self.state.chat.chat_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            text += f"チャット更新日時: {self.state.chat.chat_update_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            text += f"ログファイル: {ChatLog.get_logfile_name(self.state.chat)}\n"
            text += f"API: {self.state.settings.chat['api']}\n"
            text += f"モデル: {self.state.settings.chat['model']}\n"
            text += "---\n"
            text += "\n"

        for message in self.state.chat.messages:
            role = message["role"]
            if role == "user":
                name = self.state.settings.user["name"]
            elif role == "assistant":
                name = self.state.settings.assistant["name"]
            else:
                continue

            text += f"## {name}\n\n"
            text += f"{message['content']}\n\n"
        return text

    # チャットの内容を要約する
    def summarize_chat(self):
        messages = self.get_all_message_text(add_header=False)
        lang = langdetect.detect(messages)
        query = get_text_resource("SUMMARIZE_PROMPT", lang) + messages

        try:
            summary = self.state.chat.send_onetime_message(query)

            # 回答全体がコードブロックで囲まれていたら、それを外す
            pattern = r'```[a-zA-Z]*\n(.*?)\n```'
            match = re.search(pattern, summary, re.DOTALL)
            if match:
                summary = match.group(1)

            return summary
        except Exception as e:
            location = get_location(self)
            error_type = get_exception_name(e)
            AppLogger.error(f"Failed to summarize chat")
            AppLogger.error(f"  -> location : {location}")
            AppLogger.error(f"  -> exception : {error_type}")
            print(e)
            return ""

    # スピーカーのON/OFFを切り替えるイベントハンドラ（UI）
    def toggle_speaker(self):
        self.app_config.system["speaker_on"] = not self.app_config.system["speaker_on"]
        self.app_config.save()

    # チャットのリプレイ
    def replay(self):
        def process_sentence(sentence: str):
            self.window.js.addReplayMessage(sentence)

            sentence = sentence.strip()
            if sentence == "":
                return

            if message["role"] == "assistant":
                self.state.assistant_character.talk(sentence)
            else:
                self.state.user_character.talk(sentence)

        for message in self.state.chat.messages:
            self.window.js.startReplayMessageBlock(message["role"])
            sentence: str = ""
            for c in message["content"]:
                sentence += c
                if sentence.endswith(("。", "\n", "？", "！")):
                    process_sentence(sentence)
                    sentence = ""
            
            if sentence != "":
                process_sentence(sentence)

            self.window.js.endReplayMessageBlock(message["content"])

        self.window.js.setChatMessages(self.state.chat.messages)

    # TTS用キャラクターを作成する（ユーザー）
    def create_user_character(self):
        param = copy.deepcopy(self.state.settings.user)
        return self.create_character(param)

    # TTS用キャラクターを作成する（アシスタント）
    def create_assistant_character(self):
        param = copy.deepcopy(self.state.settings.assistant)
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
                    self.window.js.handleChatException(message)
                    character = None

        return character

    # チャンク受信イベントハンドラ（Chat）
    def on_recieve_chunk(self, chunk: str):
        self.window.js.addChunk(chunk)

    # センテンス読み上げイベントハンドラ（Chat）
    def on_recieve_sentence(self, sentence: str):
        if self.state.assistant_character is not None and self.app_config.system["speaker_on"]:
            self.state.assistant_character.talk(sentence)
        self.window.js.parsedSentence(sentence)

    # 段落受信イベントハンドラ（Chat）
    def on_recieve_paragraph(self, paragraph: str):
        self.window.js.parsedParagraph(paragraph)

    # レスポンス受信完了イベントハンドラ（Chat）
    def on_end_response(self, content: str):
        ChatLog.save(self.state.settings, self.state.chat)
        self.window.js.endResponse(content)

    # チャット例外イベントハンドラ（Chat）
    def on_chat_error(self, e: Exception, cause: str, info: str=""):
        location = get_location(self)
        error_type = get_exception_name(e)
        AppLogger.error(f"{cause} : {info}")
        AppLogger.error(f"  -> location : {location}")
        AppLogger.error(f"  -> exception : {error_type}")
        print(e)

        if cause == "Timeout":
            message = get_text_resource("ERROR_API_TIMEOUT")
            self.window.js.handleChatTimeoutException(message)
        else:
            if cause == "Authentication":
                message = get_text_resource("ERROR_API_AUTHENTICATION_FAILED")
            elif cause == "EndPointNotFound":
                message = get_text_resource("ERROR_API_ENDPOINT_INCORRECT")
            elif cause == "UnsafeContent":
                message = get_text_resource("ERROR_CONVERSATION_CONTENT_INAPPROPRIATE")
            elif cause == "RateLimit":
                message = get_text_resource("ERROR_RATE_LIMIT_REACHED")
            elif cause == "APIError":
                message = get_text_resource("ERROR_API_ERROR_OCCURRED") + f"\n{info}"
            else:
                message = get_text_resource("ERROR_UNKNOWN_OCCURRED") + f"（{error_type}）"
            self.window.js.handleChatException(message)
