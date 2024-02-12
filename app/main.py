# ZundaGPT2
#
# メイン
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import copy

import webview

from settings import Settings
from chat import ChatFactory
from chat import Chat
from character import CharacterVoicevox
from character import CharacterCoeiroink
from character import CharacterAIVoice
from chat_log import ChatLog

APP_NAME = "ZundaGPT2"
APP_VERSION = "0.1.0"
COPYRIGHT = "Copyright 2024 led-mirage"

# アプリケーションクラス
class Application:
    # コンストラクタ
    def __init__(self, chat: Chat, settings: Settings):
        self.chat = chat
        self.settings = settings
        self.user_character = self.create_user_character()
        self.assistant_character = self.create_assistant_character()
        self.chat_log = ChatLog(settings)
    
    # 開始する
    def start(self):
        window_title = f"{APP_NAME}  ver {APP_VERSION}"
        self.window = webview.create_window(window_title, url="html/index.html", width=600, height=800, js_api=self, text_select=True)
        webview.start()

    # ページロードイベントハンドラ（UI）
    def page_loaded(self):
        self.window.evaluate_js(f"setUsername('{self.settings.user["name"]}', '{self.settings.user["name_color"]}')")

    # メッセージ送信イベントハンドラ（UI）
    def send_message_to_chatgpt(self, text):
        self.user_character.talk(text)
        self.window.evaluate_js(f"startResponse('{self.settings.assistant["name"]}', '{self.settings.assistant["name_color"]}')")
        self.chat.send_message(text, self.recieve_chunk, self.recieve_sentence, self.end_response)

    # チャンク受信イベントハンドラ（Chat）
    def recieve_chunk(self, chunk):
        self.window.evaluate_js(f"addChunk('{self.escape_js_string(chunk)}')")
        #print(chunk, end="", flush=True)

    # センテンス読み上げイベントハンドラ（Chat）
    def recieve_sentence(self, sentence):
        self.assistant_character.talk(sentence)
        # センテンスごとに改行したい場合
        #if not sentence.endswith("\n"):
        #    self.window.evaluate_js(f"addChunk('{self.escape_js_string("\n")}')")
        #    print()
    
    # レスポンス受信完了イベントハンドラ（Chat）
    def end_response(self, response):
        self.chat_log.save(chat)
        #print()

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
    settings = Settings("settings.json")
    settings.load()

    chat = ChatFactory.create(
        settings.chat["api"],
        settings.chat["model"],
        settings.chat["instruction"],
        settings.chat["bad_response"],
        settings.chat["history_size"]
    )

    app = Application(chat, settings)
    app.start()
