# ZundaGPT2
#
# 言語サポート
#
# Copyright (c) 2024-2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

# テキストリソースの定義
text_resources = {
    "ja": {
        "ERROR_MISSING_OPENAI_API_KEY": "環境変数 OPENAI_API_KEY が設定されていません。",
        "ERROR_MISSING_AZURE_OPENAI_ENDPOINT": "環境変数 AZURE_OPENAI_ENDPOINT が設定されていません。",
        "ERROR_MISSING_AZURE_OPENAI_API_KEY": "環境変数 AZURE_OPENAI_API_KEY が設定されていません。",
        "ERROR_MISSING_GEMINI_API_KEY": "環境変数 GEMINI_API_KEY が設定されていません。",
        "ERROR_MISSING_ANTHROPIC_API_KEY": "環境変数 ANTHROPIC_API_KEY が設定されていません。",
        "ERROR_API_ID_IS_INCORRECT": "API IDが間違っています。",
        "ERROR_API_TIMEOUT": "APIの呼び出しがタイムアウトしたのだ",
        "ERROR_API_AUTHENTICATION_FAILED": "APIの認証に失敗したのだ",
        "ERROR_API_ENDPOINT_INCORRECT": "APIのエンドポイントが間違っているのだ",
        "ERROR_CONVERSATION_CONTENT_INAPPROPRIATE": "会話の内容が不適切だと判断されたのだ",
        "ERROR_RATE_LIMIT_REACHED": "レート制限に達したのだ",
        "ERROR_API_ERROR_OCCURRED": "APIエラーが発生したのだ",
        "ERROR_UNKNOWN_OCCURED": "なんかわからないエラーが発生したのだ",
        "ERROR_GOOGLETTS_FFMPEG_NOT_FOUND": "Google Text-to-Speechを使用するには、あらかじめFFmpegをインストールしておく必要があります\n\nFFmpegをインストールしてパスを通しておいてください",
    },
    "en": {
        "ERROR_MISSING_OPENAI_API_KEY": "The environment variable OPENAI_API_KEY is not set.",
        "ERROR_MISSING_AZURE_OPENAI_ENDPOINT": "The environment variable AZURE_OPENAI_ENDPOINT is not set.",
        "ERROR_MISSING_AZURE_OPENAI_API_KEY": "The environment variable AZURE_OPENAI_API_KEY is not set.",
        "ERROR_MISSING_GEMINI_API_KEY": "The environment variable GEMINI_API_KEY is not set.",
        "ERROR_MISSING_ANTHROPIC_API_KEY": "The environment variable ANTHROPIC_API_KEY is not set.",
        "ERROR_API_ID_IS_INCORRECT": "API ID is incorrect.",
        "ERROR_API_TIMEOUT": "The API call timed out.",
        "ERROR_API_AUTHENTICATION_FAILED": "Failed to authenticate the API.",
        "ERROR_API_ENDPOINT_INCORRECT": "The API endpoint is incorrect.",
        "ERROR_CONVERSATION_CONTENT_INAPPROPRIATE": "The content of the conversation was deemed inappropriate.",
        "ERROR_RATE_LIMIT_REACHED": "Rate limit reached.",
        "ERROR_API_ERROR_OCCURRED": "An API error occurred.",
        "ERROR_UNKNOWN_OCCURED": "An unknown error has occurred.",
        "ERROR_GOOGLETTS_FFMPEG_NOT_FOUND": "To use Google Text-to-Speech, you need to install FFmpeg beforehand.\n\nPlease install FFmpeg and ensure that it is added to the system path.",
    }
}

# 現在の言語を保存する変数
current_language = "ja"

# 言語を設定する関数
def set_current_language(language):
    global current_language
    current_language = language
    if language in text_resources:
        current_language = language
    else:
        print(f"Warning: '{language}' is not a valid language code. Defaulting to 'en'.")
        current_language = "en"

# テキストリソースを取得する関数
def get_text_resource(key):
    return text_resources.get(current_language, {}).get(key, key)
