# ZundaGPT2
#
# VOICEVOXキャラクター一覧資料作成
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import sys
sys.path.append("./")

from app.voiceapi.voicevox_api import VoicevoxAPI

def write(file, text=""):
    file.write(text + "\n")
    print(text)

with open("voicevox_speaker_list.md", "w", encoding="utf-8") as file:
    write(file, "# VOICEVOX キャラクターリスト")
    write(file)

    write(file, f"## VOICEVOX Engine Version {VoicevoxAPI.get_version()}")
    write(file)

    speakers = VoicevoxAPI.get_speakers()

    write(file, "| ID | キャラクター | スタイル |")
    write(file, "|----|--------------|----------|")
    for speaker in speakers:
        write(file, f"| {speaker.id} | {speaker.name} | {speaker.style_name} |")
