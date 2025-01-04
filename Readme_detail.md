# ZundaGPT2　追加資料

Copyright (c) 2024-2025 led-mirage

## はじめに

この追加資料では、より詳しい情報を記載しているのだ。

- [アプリを動かすのに必要なもの](#アプリを動かすのに必要なもの)
- [設定ファイル](#設定ファイル)
- [通信先](#通信先)

## アプリを動かすのに必要なもの

### ✅ OpenAIアカウントとAPIキー

チャットの部分はOpenAIのAIを使用しているので、OpenAIのアカウントとAPIの利用登録（課金およびAPIキーの作成）が必要なのだ。

アカウントを作成すると、作ってから３ヵ月間有効な無料枠（$18）があるようなので、それを使ってもいいのだ。ボクの場合は利用開始から３ヵ月以上経ってしまっていたので、無料枠は利用できなくて、仕方ないから$10課金したのだ。

APIキーの作成は特に難しくないのだ。OpenAI APIの設定画面に入って、左側の`API Keys`というメニューから新しいAPIキーを作成すればいいのだ。作成するときに表示されるAPIキーは、作成後には２度と表示できないからメモ帳などにコピペして保存しておくといいのだ。このキーはあとから設定に必要になるのだ。

OpenAI … https://platform.openai.com/

### ✅ Google Gemini APIのAPIキー

バージョン0.11.0からGoogle Gemini APIにも対応したので、OpenAIの代わりにGoogle Gemini APIを使用することもできるのだ。

現時点でGoogle Gemini APIには無料プランが設定されているので、OpenAIのAPIよりも気軽に利用することができるのだ。Google Gemini APIを使用したい場合は、[専用の資料](Readme_gemini.md)を用意したので、それを参照して欲しいのだ。

### ✅ Anthropic APIのAPIキー

バージョン1.4.0からAnthropic API（Claudeシリーズ）にも対応したのだ。APIを利用するには[Anthropic Console](https://console.anthropic.com/)のアカウントとAPIの利用登録（課金およびAPIキーの作成）が必要なのだ。

### ✅ VOICEVOX（オプション）

ずんだもんやVOICEVOXに入っている他のキャラクターの声でチャットを読み上げてもらうには、あらかじめVOICEVOXをインストールしておく必要があるのだ。VOICEVOXは公式サイトからダウンロードして簡単にインストールできるのだ。

VOICEVOXのユーザーインターフェイスが不要な人は、VOICEVOX Engineを利用することもできるのだ。少し玄人向けなので、分からない人は素直にVOICEVOXを利用するのがお勧めなのだ。

VOICEVOX … https://voicevox.hiroshiba.jp/  
VOICEVOX Engine … https://github.com/VOICEVOX/voicevox_engine

### ✅ COEIROINK（オプション）

COEIROINKはVOICEVOXと同じ無料のテキスト読み上げソフトウェアなのだ。COEIROINKをダウンロードしてインストールしておけば、ZundaGPT2でも使えるのだ。

COEIROINK … https://coeiroink.com/

### ✅ A.I.VOICE（オプション）

A.I.VOICEで話してもらうにはA.I.VOICEを購入してインストールしておく必要があるのだ。購入方法、インストール方法などは公式ページを見て欲しいのだ。もうすでに持っている人は使ってみて欲しいのだ。

ちなみにA.I.VOICE2には対応していないので注意してなのだ。

A.I.VOICE … https://aivoice.jp/

### ✅ Google Text-to-Speech（オプション）

Google製のTTSエンジンなのだ。Googleとサーバーと通信して発音する音声データを取得するのだ。そのため、他のローカルPC上で動作するTTSエンジンと比べると、発音するまでに時間がかかるのだ。いい点としては、非常に多くの言語に対応していることが挙げられるのだ。

作者の環境では動作が遅くてこのアプリには不向きだと思ったけど、せっかく作ったから搭載しておくのだ。

Google Text-to-Speechを使うには、FFmepgを別途インストールしておく必要があるのだ。公式サイトのリンクからダウンロードして、保存したフォルダにパスを通しておくのだ。

### ✅ SAPI5（オプション）

SAPI5は、Microsoftの音声認識や音声合成のAPIなのだ。Windowsの標準機能だから、何もインストールしなくても使えるのだ。ただし、日本語の声質はそこまでよくないので、ほかのアプリをインストールしたくない人向きの選択肢なのだ。

## 設定ファイル

設定ファイルは２つあるのだ。ひとつはシステムの設定が書かれているapp_config.json。もうひとつはチャットするキャラクターの情報が書かれているsettings.jsonなのだ。

### ⚙️ app_config.json

#### ✨ system/log_folder（既定値 log）

チャットのログファイルを保存するフォルダを指定するのだ。この値が空文字の場合はログは保存されないのだ。

#### ✨ system/settings_file（既定値 settings.json）

新規チャットを開始したときに使われるキャラクター設定ファイルを指定するのだ。GUIから変更できるのだ。

#### ✨ system/speaker_on（既定値 true）

会話を読み上げるかどうかの設定なのだ。GUIから変更できるのだ。

#### ✨ system/window_width（既定値 600）

ウィンドウの幅の初期値なのだ。

#### ✨ system/window_height（既定値 800）

ウィンドウの高さの初期値なのだ。

#### ✨ system/chat_api_timeout（既定値 30）

Chat APIのタイムアウト値を秒数で指定するのだ。

#### ✨ tts/voicevox_server（既定値 http://127.0.0.1:50021）

VOICEVOXのサーバーのURLを記載するのだ。これがVOICEVOXのデフォルトなので、普通はここを変更する必要はないのだ。分かる人はわかると思うんだけど、このIPは自PCのIPになっているのだ。他のPCで実行しているVOICEVOXに声を生成してもらう場合は、このURLを変更すればいいのだ。ただ、ファイアウォールの設定とかいろいろ面倒なので、分からない人は気にする必要はないのだ。

#### ✨ tts/voicevox_path（既定値 %LOCALAPPDATA%/Programs/VOICEVOX/VOICEVOX.exe）

VOICEVOXの実行ファイルのパスを記載するのだ。この項目がない場合は、VOICEVOXのWindowsへの既定のインストール先が使われるのだ。

#### ✨ tts/coeiroink_server（既定値 http://127.0.0.1:50032）

VOICEVOXのサーバーのURLを記載するのだ。これがVOICEVOXのデフォルトなので、普通はここを変更する必要はないのだ。分かる人はわかると思うんだけど、このIPは自PCのIPになっているのだ。他のPCで実行しているVOICEVOXに声を生成してもらう場合は、このURLを変更すればいいのだ。ただ、ファイアウォールの設定とかいろいろ面倒なので、分からない人は気にする必要はないのだ。

#### ✨ tts/coeiroink_path（既定値 空文字）

COEIROINKの実行ファイルのパスを記載するのだ。COEIROINKは既定のインストール場所がないから、自分がインストールした場所（解凍した場所）を記載するのだ。例えば次のように記載するのだ。

```json
"coeiroink_path": "C:/Program Files/COEIROINK_GPU/COEIROINKv2.exe"
```

なんのことかわからない人は、COEIROINKを起動してから、ずんだGPTを使えば問題ないのだ。

#### ✨ tts/aivoice_path（既定値 %ProgramW6432%/AI/AIVoice/AIVoiceEditor/AI.Talk.Editor.Api.dll）

A.I.VOICEのDLLのパスを記載するのだ。この項目がない場合は、A.I.VOICEの既定のインストール先の設定が使われるのだ。

#### ✨ gemini/safty_filter_harassment（既定値 BLOCK_MEDIUM_AND_ABOVE）

Gemini用の安全性フィルタ設定なのだ。ハラスメントに関するしきい値を設定できるのだ。詳しくは[こちらの資料](Readme_gemini.md)を参照して欲しいのだ。

#### ✨ gemini/safty_filter_hate_speech（既定値 BLOCK_MEDIUM_AND_ABOVE）

Gemini用の安全性フィルタ設定なのだ。ヘイトスピーチに関するしきい値を設定できるのだ。詳しくは[こちらの資料](Readme_gemini.md)を参照して欲しいのだ。

#### ✨ gemini/safty_filter_sexually_explicit（既定値 BLOCK_MEDIUM_AND_ABOVE）

Gemini用の安全性フィルタ設定なのだ。性表現に関するしきい値を設定できるのだ。詳しくは[こちらの資料](Readme_gemini.md)を参照して欲しいのだ。

#### ✨ gemini/safty_filter_dangerous_content（既定値 BLOCK_MEDIUM_AND_ABOVE）

Gemini用の安全性フィルタ設定なのだ。危険な内容に関するしきい値を設定できるのだ。詳しくは[こちらの資料](Readme_gemini.md)を参照して欲しいのだ。

### ⚙️ settings.json

settings.jsonはsettingsフォルダの中に格納されているのだ。声のキャラクターを変えたいときなどは、このファイルを編集するといいのだ。また、このファイルをコピーして別の名前を付けて保存することで、複数の設定を保存しておくことができるのだ。設定を切り替えるには、ウィンドウの設定ボタンを押すといいのだ。

#### ✨ user/name（既定値 あなた）

あなたの名前の設定なのだ。

#### ✨ user/name_color（既定値 #007bff）

あなたの名前の色の設定なのだ。

#### ✨ user/icon（既定値 空文字）

発言者名の横に表示するアイコンの設定なのだ。PNG形式の画像ファイルを指定できるのだ。空文字にするとアイコンは表示されないのだ。

例：chat_icons/user_black.png

chat_iconsフォルダの中にいくつかアイコン用の画像を用意してあるのだ。

#### ✨ user/tts_software（既定値 VOICEVOX）

あなたのメッセージのテキスト読み上げに使用するソフトウェアを選択するのだ。設定できる値は、"VOICEVOX"、"COEIROINK"、"AIVOICE"、"GTTS"、"SAPI5"、もしくはテキストを読み上げない場合に使用する""の６つなのだ。

#### ✨ user/speaker_id（既定値 13）

あなたの声のIDなのだ。VOICEVOXの場合、"13"は青山龍星を意味しているのだ。VOICEVOXに収録されている他のキャラクターの声で話して欲しいときは、この値を変更すればいいのだ。キャラクターのIDを調べるには、[この資料](doc/voicevox_speaker_list.md)を参考にするといいのだ。

COEIROINKの場合、ここにはキャラクターのStyleIdを指定するのだ。StyleIdは[この資料](doc/coeiroink_speaker_list.md)を参考にしてほしいのだ。ただこの資料に載っているのは一部のキャラクターのみなのだ。使いたいキャラのStyleIdを調べるには、tool/coeiroink_speaker_list.pyを実行してほしいのだ。

A.I.VOICEの場合、ここにはキャラクターの名前かプリセットの名前を設定すればいいのだ。例えば、"琴葉 茜"とかを設定すればいいのだ。

Google Text-to-Speech(GTTS)の場合は、キャラクターが選択できないので空欄でいいのだ。

SAPI5の場合は、"Haruka"や"Ayumi"、"Sayaka"などのキャラクター名を設定するのだ。英語を発音させたい場合は"Zira"なども使えるのだ。

#### ✨ user/speed_scale（既定値 1.2）

あなたの声の読み上げの速さの設定なのだ。VOICEVOXのデフォルトは1.0なんだけど、ボクは少し早く読み上げさせたかったので1.2としているのだ。遅くしたい場合はこの値を減らせばいいのだ。

A.I.VOICEの場合、この設定は無効なのだ。読み上げ方はA.I.VOICE Editor側のプリセットで調整して欲しいのだ。

GTTSの場合、この設定は無効なのだ。

SAPIの場合は話速を-10～10の範囲で指定できるのだ。0が標準速度なのだ。

#### ✨ user_pitch_scale（既定値 0.0）

あなたの声の高さの設定なのだ。この値を増やすと、声の高さが上がるのだ。ただ、少しの変化で大きく変わるので、0.1とか0.2とか小刻みに調整するといいのだ。

A.I.VOICEの場合、この設定は無効なのだ。読み上げ方はA.I.VOICE Editor側のプリセットで調整して欲しいのだ。

GTTS、SAPI5の場合も、この設定は無効なのだ。

#### ✨ assistant/name（既定値 ずんだ）

チャットアシスタントの名前の設定なのだ。

#### ✨ assistant/name_color（既定値 #006400）

チャットアシスタントの名前の色の設定なのだ。

#### ✨ assistant/icon（既定値 空文字）

発言者名の横に表示するアイコンの設定なのだ。PNG形式の画像ファイルを指定できるのだ。空文字にするとアイコンは表示されないのだ。

例：chat_icons/zunda_lime.png

chat_iconsフォルダの中にいくつかアイコン用の画像を用意してあるのだ。

#### ✨ assistant/tts_software（既定値 VOICEVOX）

チャットアシスタントのテキスト読み上げに使用するソフトウェアを選択するのだ。設定できる値は、"VOICEVOX"、"COEIROINK"、"AIVOICE"、"GTTS"、"SAPI5"、もしくはテキストを読み上げない場合に使用する""の６つなのだ。

#### ✨ assistant/speaker_id（既定値 3）

チャットアシスタントの声のIDなのだ。VOICEVOXの場合、"3"はずんだもんを意味しているのだ。VOICEVOXに収録されている他のキャラクターの声で話して欲しいときは、この値を変更すればいいのだ。キャラクターのIDを調べるには、[この資料](doc/voicevox_speaker_list.md)を参考にするといいのだ。

COEIROINKの場合、ここにはキャラクターのStyleIdを指定するのだ。StyleIdは[この資料](doc/coeiroink_speaker_list.md)を参考にしてほしいのだ。ただこの資料に載っているのは一部のキャラクターのみなのだ。使いたいキャラのStyleIdを調べるには、tool/coeiroink_speaker_list.pyを実行してほしいのだ。

A.I.VOICEの場合、ここにはキャラクターの名前かプリセットの名前を設定すればいいのだ。例えば、"琴葉 茜"とかを設定すればいいのだ。

Google Text-to-Speech(GTTS)の場合は、キャラクターが選択できないので空欄でいいのだ。

SAPI5の場合は、"Haruka"や"Ayumi"、"Sayaka"などのキャラクター名を設定するのだ。英語を発音させたい場合は"Zira"なども使えるのだ。

#### ✨ assistant/speed_scale（既定値 1.2）

チャットアシスタントの読み上げの速さの設定なのだ。VOICEVOXのデフォルトは1.0なんだけど、ボクは少し早く読み上げさせたかったので1.2としているのだ。遅くしたい場合はこの値を減らせばいいのだ。

A.I.VOICEの場合、この設定は無効なのだ。読み上げ方はA.I.VOICE Editor側のプリセットで調整して欲しいのだ。

GTTSの場合、この設定は無効なのだ。

SAPIの場合は話速を-10～10の範囲で指定できるのだ。0が標準速度なのだ。

#### ✨ assistant/pitch_scale（既定値 0.0）

チャットアシスタントの声の高さの設定なのだ。この値を増やすと、声の高さが上がるのだ。ただ、少しの変化で大きく変わるので、0.1とか0.2とか小刻みに調整するといいのだ。

A.I.VOICEの場合、この設定は無効なのだ。読み上げ方はA.I.VOICE Editor側のプリセットで調整して欲しいのだ。

GTTS、SAPI5の場合も、この設定は無効なのだ。

#### ✨ chat/api（既定値 OpenAI）

使用するAPIの設定なのだ。設定できる値は`OpenAI`と`AzureOpenAI`と`Gemini`と`Claude`の４つなのだ。

使用するAPIによって設定しないといけない環境変数が異なるから注意して欲しいのだ。

**OpenAI**

| 変数名 | 値 |
|------|------|
| OPENAI_API_KEY  | OpenAIで取得したAPIキー |

**AzureOpenAI**

| 変数名 | 値 |
|------|------|
| AZURE_OPENAI_ENDPOINT | Azure OpenAI Serviceの通信先（エンドポイント）|
| AZURE_OPENAI_API_KEY  | Azureで取得したAPIキー |

**Gemini**

| 変数名 | 値 |
|------|------|
| GEMINI_API_KEY  | Googleで取得したAPIキー |

**Claude**

| 変数名 | 値 |
|------|------|
| ANTHROPIC_API_KEY  | Anthropicで取得したAPIキー |

#### ✨ chat/model（既定値 gpt-3.5-turbo-0125）

使用するAIのモデル名を指定するのだ。使用するAPIによって指定できるモデル名が異なるので注意して欲しいのだ。

**OpenAI**

既定はリーズナブルなGTP3.5を使用しているのだ。もっと賢くしたい場合はGPT4.0系も使えるけれど、その分利用量が上がるので注意するのだ。使用できるモデルの一覧と利用料金は以下のリンクで確認できるのだ。

モデルの一覧 … https://platform.openai.com/docs/models  
利用料金 … https://openai.com/pricing#language-models

**AzureOpenAI**

Azure上でモデルをデプロイする際につけてモデル名を指定するのだ。

**Gemini**

Geminiでは以下のモデル名を指定できるのだ。詳しくは、[こちらの資料](Readme_gemini.md)を参照して欲しいのだ。

- gemini-1.0-pro-latest
- gemini-1.5-flash-latest
- gemini-1.5-pro-latest

**Claude**

Anthropicの場合、2024年12月29日時点で、以下のモデルを指定できるのだ。

- Claude 3.5 Sonnet 2024-10-22
- Claude 3.5 Sonnet 2024-06-20
- Claude 3.5 Haiku
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku

#### ✨ chat/instraction（既定値 君は優秀なアシスタント…以下略）

AIのキャラづけの設定なのだ。ここで、AIの台詞をずんだもんっぽくするようお願いしているのだ。ここを変更することで、ずんだもん以外のキャラクターっぽい回答を生成することも可能なのだ。

#### ✨ chat/bad_response（既定値 答えられないのだ）

何らかの原因でAIが回答できなかった場合に表示するセリフを設定するのだ。無理なお願いをするとAIが答えてくれない場合があるから気を付けるといいのだ。

#### ✨ chat/history_size（既定値 6）

AIに送信する過去の会話の履歴数を設定するのだ。この値が大きいほど前の回答、質問を考慮した回答をAIが生成するようになって、会話のつながりがよくなるのだ。ただ、その分利用料金も増えるので注意が必要なのだ。

この設定がある理由を考えればわかるけど、AIは過去の会話を覚えていないのだ。質問をするたびに、過去の会話もAIに送信することで、AIは会話のつながりを知ることができるのだ。ただ利用料金は送信するデータ量が増えるとその分加算されるので、バランスをとることが大事なのだ。

## 通信先

このアプリの通信先は以下の通りなのだ。

### 🌐 OpenAI API（HTTPS）

chat/apiに`OpenAI`を指定した場合は、チャットの回答を取得するために OpenAIのサーバーと通信を行うのだ。通信方法は、OpenAIのライブラリを使用しているのだ。

### 🌐 Azure OpenAI Service（HTTPS）

chat/apiに`AzureOpenAI`を指定した場合は、チャットの回答を取得するために Microsoft Azure OpenAI Serviceと通信を行うのだ。通信方法は、OpenAIのライブラリを使用しているのだ。

### 🌐 Google Gemini API（HTTPS）

chat/apiに`Gemini`を指定した場合は、チャットの回答を取得するために Googleのサーバーと通信を行うのだ。通信方法は、Googleのライブラリを使用しているのだ。

### 🌐 Anthropic API（HTTPS）

chat/apiに`Claude`を指定した場合は、チャットの回答を取得するために Anthropicのサーバーと通信を行うのだ。通信方法は、Anthropicのライブラリを使用しているのだ。

### 🌐 Google TTS API（HTTPS）

tts_softwareにGTTSを指定した場合は、テキストを音声データの変換するためにGoogleのサーバーと通信を行うのだ。通信方法は、gTTSライブラリを使用しているのだ。

### ➰ VOICEVOX ローカルサーバー（HTTP）

テキストを音声データに変換するために、VOICEVOXのローカルサーバーと通信を行っているのだ。既定のエンドポイントは `http://127.0.0.1:50021` なのだ。

### ➰ COEIROINK ローカルサーバー（HTTP）

テキストを音声データに変換するために、VOICEVOXのローカルサーバーと通信を行っているのだ。既定のエンドポイントは `http://127.0.0.1:50032` なのだ。

### ➰ A.I.VOICE API

テキストを音声データに変換するために、A.I.VOICE Editor APIを使用しているのだ。通信方法は明記されていないけど、名前付きパイプかなにかを使っているんじゃないかな（てきとー）。

### ➰ pywebview（TCP）

このアプリではGUIをpywebviewで作ってるんだけど、UI(HTML)とバックエンドのPythonプログラムとの連携をとるのにTCPでリスニングしているみたい。詳しいことはわからないのだ。

## ファイル入出力

### 🗒️ 設定ファイル（appConfig.json）

システムの設定を記載したファイル。初回起動時に自動的に作成されるのだ。

### 🗒️ 設定ファイル（settings.json）

チャットするキャラクターの情報を記載したファイル。これも、初回起動時に自動的に作成されるのだ。

### 🗒️ チャットログファイル（chatlog-yyyymmdd-hhmmss.json）

チャットの内容を記載したファイル。ファイル名の日時はチャットを開始した日時なのだ。

