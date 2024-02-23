# ZundaGPT2
#
# VOICEキャラクターモジュール
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import os
import subprocess
import time

import clr

from sound import play_sound
from voiceapi import VoicevoxAPI
from voiceapi import CoeiroinkApi

# VOICEVOXキャラクター
class CharacterVoicevox:
    DEFAULT_INSTALL_PATH = "%LOCALAPPDATA%/Programs/VOICEVOX/VOICEVOX.exe"

    # コンストラクタ
    def __init__(self, speaker_id, speed_scale, pitch_scale, voicevox_path=DEFAULT_INSTALL_PATH):
        self.voicevox_path = voicevox_path
        self.speaker_id = speaker_id
        self.speed_scale = speed_scale
        self.pitch_scale = pitch_scale
        if self.voicevox_path != "":
            CharacterVoicevox.run_voicevox(self.voicevox_path)

    # 話す
    def talk(self, text):
        if CharacterVoicevox.run_voicevox(self.voicevox_path):
            wave_data = VoicevoxAPI.get_wave_data(self.speaker_id, text, self.speed_scale, self.pitch_scale)
            if wave_data is not None:
                play_sound(wave_data)

    # VOICEVOXが起動しているかどうかを調べる
    @staticmethod
    def is_voicevox_running():
        return VoicevoxAPI.get_version() is not None

    # VOICEVOXが起動していなかったら起動する
    @staticmethod
    def run_voicevox(voicevox_path=DEFAULT_INSTALL_PATH):
        if CharacterVoicevox.is_voicevox_running():
            return True
        else:
            appdata_local = os.getenv("LOCALAPPDATA")
            voicevox_path = voicevox_path.replace("%LOCALAPPDATA%", appdata_local)
            if os.path.isfile(voicevox_path):
                subprocess.Popen(voicevox_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                loop_count = 0
                while CharacterVoicevox.is_voicevox_running() == False:
                    time.sleep(1)
                    loop_count += 1
                    if loop_count >= 10:
                        return False
                return True
            else:
                return False

# COEIROINKキャラクター
class CharacterCoeiroink:
    # コンストラクタ
    def __init__(self, speaker_id, speed_scale, pitch_scale, coeiroink_path):
        self.coeiroink_path = coeiroink_path
        self.speed_scale = speed_scale
        self.pitch_scale = pitch_scale
        self.speaker_id = speaker_id
        if self.coeiroink_path != "":
            CharacterCoeiroink.run_coeiroink(self.coeiroink_path)

    # 話す
    def talk(self, text):
        if CharacterCoeiroink.run_coeiroink(self.coeiroink_path):
            wave_data = CoeiroinkApi.get_wave_data(
                self.speaker_id, text, speedScale=self.speed_scale, pitchScale=self.pitch_scale, volumeScale=0.8)
            if wave_data is not None:
                play_sound(wave_data)

    # COEIROINKが起動しているかどうかを調べる
    @staticmethod
    def is_coeiroink_running():
        return CoeiroinkApi.get_status() is not None

    # COEIROINKが起動していなかったら起動する
    @staticmethod
    def run_coeiroink(coeiroink_path):
        if CharacterCoeiroink.is_coeiroink_running():
            return True
        else:
            if os.path.isfile(coeiroink_path):
                subprocess.Popen(coeiroink_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                loop_count = 0
                while CharacterCoeiroink.is_coeiroink_running() == False:
                    time.sleep(1)
                    loop_count += 1
                    if loop_count >= 10:
                        return False
                return True
            else:
                return False

# A.I.VOICEキャラクター
class CharacterAIVoice:
    DEFAULT_INSTALL_PATH = "%ProgramW6432%/AI/AIVoice/AIVoiceEditor/AI.Talk.Editor.Api.dll"

    _tts_control = None

    # コンストラクタ
    def __init__(self, speaker_id, aivoice_path= DEFAULT_INSTALL_PATH):
        self.speaker_id = speaker_id
        self.aivoice_path = aivoice_path
        CharacterAIVoice.run_aivoice(self.aivoice_path)

    # 話す
    def talk(self, text):
        CharacterAIVoice.run_aivoice(self.aivoice_path)
        try:
            tts_control = CharacterAIVoice._tts_control
            tts_control.Connect()
            tts_control.CurrentVoicePresetName = self.speaker_id
            tts_control.Text = text
            play_time = tts_control.GetPlayTime()
            tts_control.Play()
            time.sleep((play_time + 500) / 1000)
        except Exception as err:
            CharacterAIVoice._tts_control = None
            print(err)
            raise

    # A.I.VOICEが起動していなかったら起動して接続する
    @classmethod
    def run_aivoice(cls, aivoice_path=DEFAULT_INSTALL_PATH):
        program_dir = os.getenv("ProgramW6432")
        aivoice_path = aivoice_path.replace("%ProgramW6432%", program_dir)
        if os.path.isfile(aivoice_path):
            if CharacterAIVoice._tts_control is None:
                clr.AddReference(aivoice_path)
                from AI.Talk.Editor.Api import TtsControl, HostStatus

                tts_control = TtsControl()
                host_name = tts_control.GetAvailableHostNames()[0]
                tts_control.Initialize(host_name)        
                if tts_control.Status == HostStatus.NotRunning:
                    tts_control.StartHost()
                tts_control.Connect()
                cls._tts_control = tts_control

