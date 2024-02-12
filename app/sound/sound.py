# ZundaGPT2
#
# WAVEデータ作成モジュール
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import io
import wave

import pyaudio

# 音声データを再生する
def play_sound(wave_data: bytes):
    wave_file = wave.open(io.BytesIO(wave_data), 'rb')
    audio = pyaudio.PyAudio()

    try:
        format = audio.get_format_from_width(wave_file.getsampwidth())

        stream = audio.open(
            format=format,
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True)

        data = wave_file.readframes(1024)
        while data != b'':
            stream.write(data)
            data = wave_file.readframes(1024)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        wave_file.close()
