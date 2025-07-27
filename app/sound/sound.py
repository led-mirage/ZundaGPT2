# ZundaGPT2
#
# WAVEデータ作成モジュール
#
# Copyright (c) 2024-2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import io
import platform
import os
import tempfile
import time
import wave


# 音声データを再生する
def play_sound(wave_data: bytes):
    if platform.system() == "Windows":
        import pyaudio # type: ignore
        
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
            time.sleep(0.2)
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            wave_file.close()
    else:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp.write(wave_data)
            tmp.flush()
            tmpname = tmp.name
        try:
            os.system(f'aplay "{tmpname}"')
        finally:
            os.remove(tmpname)
