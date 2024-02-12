# ZundaGPT2
#
# COEIROINKキャラクター一覧資料作成
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import sys
sys.path.append("./")

from app.voiceapi import CoeiroinkApi

def write(file, text=""):
    file.write(text + "\n")
    print(text)

with open("coeiroink_speaker_list.md", "w", encoding="utf-8") as file:
    write(file, "# COEIROINK キャラクターリスト")
    write(file)

    speakers = CoeiroinkApi.get_speakers()

    write(file, "| SpeakerUuid | StyleId | キャラクター | スタイル |")
    write(file, "|-------------|---------|--------------|----------|")
    for speaker in speakers:
        for style in speaker["styles"]:
            write(file, f"| {speaker["speakerUuid"]} | {style["styleId"]} | {speaker["speakerName"]} | {style["styleName"]} |")
