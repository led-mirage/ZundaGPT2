# ZundaGPT2
#
# エラー定義
#
# Copyright (c) 2024-2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

class StreamNotAllowedError(Exception):
    def __init__(self, original: Exception, detail: str | None = None):
        super().__init__(str(original))
        self.original = original
        self.detail = detail
