# <img src="assets/ZundaGPT2.ico" width="48"> ZundaGPT2

[![GitHub All Releases](https://img.shields.io/github/downloads/led-mirage/ZundaGPT2/total?color=blue)](https://github.com/led-mirage/ZundaGPT2/releases)
[![GitHub release](https://img.shields.io/github/v/release/led-mirage/ZundaGPT2)](https://github.com/led-mirage/ZundaGPT2/releases)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenAI API](https://img.shields.io/badge/OpenAI-GPT-crimson?logo=openai)](https://platform.openai.com/)
[![Anthropic Claude](https://img.shields.io/badge/Anthropic-Claude-crimson?logo=anthropic)](https://www.anthropic.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-crimson?logo=google)](https://ai.google.dev/)

Copyright (c) 2024-2025 led-mirage

[English](Readme.en.md)

## 💎 最新情報

**v1.29.0でキャラクター毎のカスタムスタイルを設定可能になったのだ**✨

キャラクター設定ファイルを編集することで、  
キャラクター毎の背景画像、テキスト色などを設定できるようになったのだよ！

## 💎 アプリの紹介と導入方法

APIを使ってAIとチャットするアプリなのだ。
キャラクターをカスタマイズできることと、VOICEVOXなどと連携して質問と回答を音声で読み上げてくれるのが特徴なのだ。

このアプリのアピールポイントは次のとおりなのだ✨

- ３大AIサービス（OpenAI、Google Gemini、Anthropic Claude）に対応
- ローカルLLM（OpenAI API互換）に対応✨
- 柔軟なキャラクターカスタマイズ機能
- メッセージ自動読み上げ機能
- マークダウン表示、TeX形式の数式表示機能
- 過去ログ管理機能
- リプレイ機能
- 印刷機能
- Raspberry Pi対応（X11/LXDE、日本語入力はIBus限定、印刷機能は非対応）
- Linux Mint対応（Cinnamon/x64、日本語入力はIBus限定、印刷機能は非対応）
- ダークモード対応
- スタイルシート（CSS）をカスタマイズ可能✨

アプリの紹介と、もっとも手軽な導入方法を[Zennの記事](https://zenn.dev/ledmirage/articles/7650f36d3a784a)にしたので、そちらも参考にしてほしいのだ✨

Raspberry Pi、Linuxへの導入に関しても[Zennの記事](https://zenn.dev/ledmirage/articles/aa64356242aefb)にしたので、そちらを参考にしてほしいのだ✨  
記事はZundaGPT2のものだけど、導入方法はほぼ同じなのだ。

<div class="page" />

## 💎 スクリーンショット

<img src="assets/ZundaGPT2_splash.png" width="200" /><br>

<img src="doc/screenshot_1.10.0.png" width="600" /><br>

↓ カスタムCSSを使って背景画像を設定した例なのだ。
<img src="doc/screenshot_1.28.0.png" width="600" /><br>

<div class="page" />

## 💎 動作確認環境

- Windows 11 Pro 23H2、24H2
- Raspberry Pi OS Bookworm 64bit
- Linux Mint 22.1 Cinnamon Edition
- Python 3.10-3.13（開発環境は 3.12.0）
- VOICEVOX 0.23.0
- A.I.VOICE Editor 1.4.10.0
- COEIROINK v.2.3.4

<div class="page" />

## 💎 対応AIモデル

動作確認済みのモデルは以下の通りなのだ。

<details><summary>OpenAI（2025/08/10現在）</summary>

- GPT-5 （モデル名：gpt-5）
- GPT-5 mini （モデル名：gpt-5-mini）
- GPT-5 nano （モデル名：gpt-5-nano）
- GPT-5 Chat （モデル名：gpt-5-chat-latest）
- GPT-4.1 （モデル名：gpt-4.1）
- GPT-4.1 mini （モデル名：gpt-4.1-mini） 無料枠あり
- GPT-4.1 nano （モデル名：gpt-4.1-nano） 無料枠あり
- GPT-4o （モデル名：gpt-4o）
- GPT-4o mini （モデル名：gpt-4o-mini） 無料枠あり
- GPT-3.5 Turbo （モデル名：gpt-3.5-turbo）
- ChatGPT-4o （モデル名：chatgpt-4o-latest）
- GPT-4o Search Preview （モデル名：gpt-4o-search-preview）
- GPT-4o mini Search Preview （モデル名：gpt-4o-mini-search-preview） 無料枠あり
- o4-mini （モデル名：o4-mini）
- o3 （モデル名：o3）
- o3-mini （モデル名：o3-mini）
- o1 （モデル名：o1）
- o1-mini （モデル名：o1-mini）

</details>

<details><summary>Anthropic Claude（2025/05/24現在）</summary>

- Claude Opus 4 （モデル名：claude-opus-4-0）
- Claude Sonnet 4 （モデル名：claude-sonnet-4-0）
- Claude Sonnet 4 Extended Thinking Mode （モデル名：claude-sonnet-4-0）
- Claude Sonnet 3.7 （モデル名：claude-3-7-sonnet-latest）
- Claude Sonnet 3.7 Extended Thinking Mode （モデル名：claude-3-7-sonnet-latest）
- Claude Haiku 3.5 （モデル名：claude-3-5-haiku-latest）
- Claude Sonnet 3.5 V2 （モデル名：claude-3-5-sonnet-latest）
- Claude Opus 3 （モデル名：claude-3-opus-latest）
- Claude Haiku 3 （モデル名：claude-3-haiku-20240307）

</details>

<details><summary>Google Gemini（2025/04/27現在）</summary>

- Gemini 2.5 Flash Preview （モデル名：gemini-2.5-flash-preview-04-17） 無料枠あり
- Gemini 2.5 Pro Preview （モデル名：gemini-2.5-pro-exp-03-25）
- Gemini 2.0 Flash （モデル名：gemini-2.0-flash） 無料枠あり
- Gemini 2.0 Flash Lite （モデル名：gemini-2.0-flash-lite） 無料枠あり
- Gemini 1.5 Flash （モデル名：gemini-1.5-flash） 無料枠あり
- Gemini 1.5 Flash 8B （モデル名：gemini-1.5-flash-8b） 無料枠あり
- Gemini 1.5 Pro （モデル名：gemini-1.5-pro）

</details>

<div class="page" />

## 💎 言語サポート

使用する言語を変更するには`appConfig.json`ファイルの`language`設定を変更すればいいのだ。

```json
"language": "en"
```

設定できる値は以下の通りなのだ。

| 設定値 | 言語 | キャラクター設定ファイル | 実装バージョン |
|-|-|-|-|
| ja | 日本語 | settings.json | 1.6.0 |
| en | 英語 | settings.en.json | 1.6.0 |
| fi | フィンランド語 | settings.fi.json | 1.10.0 |
| es | スペイン語 | settings.es.json | 1.10.0 |
| de | ドイツ語 | settings.de.json | 1.15.0 |
| fr | フランス語語 | settings.fr.json | 1.25.0 |

<div class="page" />

## 💎 必要なもの

### ✅ APIキー

このアプリを動かすには以下のいずれかのAPIキーが必要なのだ。

#### 🔑 OpenAIのAPIキー

[OpenAI Platform](https://platform.openai.com/)のアカウントとAPIの利用登録（課金およびAPIキーの作成）が必要なのだ。

#### 🔑 Google Gemini APIのAPIキー

[Google AI Studio](https://aistudio.google.com/)でAPIキーを作成する必要があるのだ。

※2025年6月時点でGoogle Gemini APIには無料プランが設定されているので、他社のAPIよりも気軽に利用することができるのだ。このことは[Zennの記事](https://zenn.dev/ledmirage/articles/23c0240691b012)にも書いたので、そちらを参照して欲しいのだ。

#### 🔑 Anthropic APIのAPIキー

[Anthropic Console](https://console.anthropic.com/login)のアカウントとAPIの利用登録（課金およびAPIキーの作成）が必要なのだ。

### ✅ テキスト読み上げソフトウェア

このアプリは以下のテキスト読み上げソフトウェアに対応しているのだ。メッセージを読み上げてもらうには、どれか一つでいいからPCにインストールしておく必要があるのだ。でもなくても動作するから、声がいらない人は不要なのだよ。

- [VOICEVOX](https://voicevox.hiroshiba.jp/)（無料）
- [COEIROINK](https://coeiroink.com/)（無料）
- [A.I.VOICE](https://aivoice.jp/)（有料・Windows Only）
- Google Text-to-Speech（無料）… FFmpegが必要
- SAPI5（無料・Windows Only）… インストール不要

用意ができたら、次の実行方法にゴーなのだ。

<div class="page" />

## 💎 実行方法

### 🛩️ 準備：OSの環境変数を追加

使用するAIのAPIキーをOSの環境変数に登録しておく必要があるのだ。

| AI | 変数名 | 値 |
|------|------|------|
| OpenAI | OPENAI_API_KEY  | OpenAIで取得したAPIキー |
| Google Gemini | GEMINI_API_KEY  | Googleで取得したAPIキー |
| Anthropic Claude | ANTHROPIC_API_KEY  | Anthropicで取得したAPIキー |

Windowsの場合は、Windowsの検索窓で「環境変数を編集」で検索すると設定画面が立ち上がるので、そこでユーザー環境変数を追加すればいいのだ。

<img src="doc/envvar.png" style="width:300px">

<div class="page" />

### 🛩️ 実行方法①：実行ファイル（EXEファイル）を使う方法

#### 1. プロジェクト用のフォルダの作成

任意の場所にプロジェクト用のフォルダを作成するのだ。

#### 2. アプリのダウンロード

以下のリンクから ZundaGPT2.ZIP をダウンロードして、作成したフォルダに展開するのだ。

https://github.com/led-mirage/ZundaGPT2/releases/tag/v1.28.0

#### 3. 実行

ZundaGPT2.exeをダブルクリックすればアプリが起動するのだ。

※起動時にスプラッシュ画面を表示したくない人は、`ZundaGPT2.ns.exe`を替わりに使ってほしいのだ。

#### 4. 注意事項

この実行ファイル（EXEファイル）は PyInstaller というライブラリを使って作成しているんだけど、割と頻繁にウィルス対策ソフトにマルウェアとかウィルスとかに誤認されるのだ。ネットとかを見るとこの問題が結構書かれているので、よくある事象のようだけど、残念なことに根本的な解決策は見つかっていないのだ。

もちろん、このアプリに悪意のあるプログラムは入っていないのだけど、気になる人は下の「Pythonで実行する方法」で実行してほしいのだ。

<div class="page" />

### 🛩️ 実行方法②：Pythonで実行する方法

#### 1. Pythonのインストール

あらかじめ Python 3.12.0 が動く環境を作っておくのだ。他のバージョンでも動くかもしれないけど、確認はしていないのだよ。

ボクは pyenv-win + venv で仮想環境を作ってそこで開発しているから、そういった方法でも問題ないのだ。

#### 2. プロジェクト用のフォルダの作成

任意の場所にプロジェクト用のフォルダを作成するのだ。

#### 3. ターミナルの起動

ターミナルかコマンドプロンプトを起動して、作成したプロジェクトフォルダに移動するのだ。

#### 4. ソースファイルのダウンロード

ZIPファイルをダウンロードして作成したフォルダに展開するのだ。  
または、Gitが使える方は以下のコマンドを実行してクローンしてもOKなのだ。

```bash
git clone https://github.com/led-mirage/ZundaGPT2.git
```

#### 5. ライブラリのインストール

コマンドプロンプトから以下のコマンドを実行して、必要なライブラリをインストールするのだ。

```bash
pip install -r requirements.txt
```

#### 6. 実行

コマンドプロンプトから以下のコマンドを実行するとアプリが起動するのだ。

```bash
python app\main.py
```

<div class="page" />

#### 7. 起動用のバッチファイル（オプション）

以下のような起動用のバッチファイルを用意しておくと便利なのだ。

```bash
start pythonw app\main.py
```

Pythonの仮想環境を使用している場合は、以下の例のようにすればOKなのだ。

```bash
call venv\scripts\activate
start pythonw app\main.py
```

<div class="page" />

## 💎 キャラクターの設定

画面右上の⚙️ボタンを押すことで、使用するキャラクターを選択することができるのだ。

いくつかのデフォルトの設定がすでにあるけれど、設定ファイルをコピーして自分で編集することで自分好みのキャラクターを作ることができるのだ。

キャラクターの設定ファイル（settings_xxx.json）はsettingsフォルダの中に格納されているから、それをコピーして編集すればOKなのだ。

詳しい設定方法は[こちら](Readme_detail.md)をみて欲しいのだ。

<div class="page" />

## 💎 カスタムCSSの設定

カスタムCSS（スタイルシート）を作成して調整することで、アプリの色味や背景画像を変更することができるのだ。  
あらかじめ決められた変数の値を変更することで、簡単にデザインを変更することができるのだよ。

スタイルシートのはファイル名はcustom.cssとし、cssフォルダの中に入れるのだ。  
※ アプリの実行ファイルを使っている場合は、実行ファイルと同じ場所にCSSフォルダを作ってね。

以下にスタイルシートの書き方の例を示すよ。  
この例は背景画像を設定する例なのだ。

```css
/* custom.css */
:root {
    /* 背景画像の設定 */
    --background-image: url("images/cloud.jpg"); /* ローカルファイルのパス、または、ネット上のURL */
    --background-image-opacity: 0.8;

    /* 画面要素の透過設定 */
    --header-bgcolor: transparent;
    --chat-messages-bgcolor: transparent;
    --header-color: ivory; /* タイトル文字色 */

    /* チャットメッセージの吹き出しの設定 */
    --message-text-bgcolor: rgba(255, 255, 255, 0.7);
    --message-text-color: #222;
    --message-text-border-radius: 10px;  
}
```

背景画像のパスにはURLの他、ローカルファイルのパスも指定できるけど、
ローカルファイルの場合は画像ファイルのサイズを1.5MBまでに抑えて欲しいのだ。
それ以上になると表示されないので注意して欲しいのだよ。

CSSを知らない人はなんのことかわからないかもしれないけど、  
上のサンプルの画像のパスさえ自分が表示したい画像のパスに変更すれば、  
とりあえず背景画像は変更できるようになるのだ。

変更可能な変数の一覧は、`app/html/css/style.css`の先頭部分を見て欲しいのだ。

<div class="page"></div>

## 💎 注意事項

### ⚡ APIの利用料金について

このアプリは無料だけど、AI各社のAPIを使うには別途料金が発生するのだ（お試し用の無料枠もあるけど）。なので、使い過ぎには注意するのだ。定期的に各社の管理サイトで現在の利用状況を確認するなどして自己管理して欲しいのだ。

### ⚡ APIキーの重要性について

各AIのAPIキーはあなただけのものなので、人に教えたらダメなのだ。流出すると悪い人に勝手に使われてしまう可能性があるのだ。もし流出してしまったら、各AIの管理サイトで現在使っているAPIキーを削除して、使えなくして欲しいのだ。

### ⚡ ウィルス対策ソフトの誤認問題

上でも書いているけれど、配布している実行ファイル（EXEファイル）が、マルウェアやウィルスに誤認されてしまうことがあるのだ。問題はPythonのプログラムを一つの実行ファイル（EXEファイル）にまとめることにあるようなのだが、回避方法がないためどうしようもないのだ。

これが嫌な人は（ボクも嫌だけど）、Python本体をインストールしてPythonから普通に実行して欲しいのだ。実行ファイルのほうが手軽だし、そのほうがPythonに詳しくない人にとっては簡単なんだけど、誤認問題がついて回ることは覚えておいて欲しいのだ

VirusTotalでのチェック結果はこちらなのだ。

- Windows版: [72個中2個のアンチウィルスエンジンで検出 :2025/09/07 v1.29.0](https://www.virustotal.com/gui/file/a3bb741599d96be59528cd12fac34780293ad8e00a4d0866c6c24fb191b66a85?nocache=1)  
- Raspberry Pi版: [62個中0個のアンチウィルスエンジンで検出 :2025/09/07 v1.29.0](https://www.virustotal.com/gui/file/aa42f3ab0b0926b729ea59c15c2c9fb23d480bf2afcc378ec0ca20bac1816ca4?nocache=1)
- Linux版: [63個中0個のアンチウィルスエンジンで検出 :2025/09/07 v1.29.0](https://www.virustotal.com/gui/file/f060f7b7c456d19fae2890937d5ebbdaa2e7fe342e647ed9dfe0a3d9f867524f?nocache=1)

<img src="doc/virustotal_1.29.0.png" width="600">

### ⚡ 免責事項

いまのところ特に問題点は見つかっていないけど、バグなんてものは潜在的に必ずあるし、０になるなんてことはあり得ないのだ。また、もしバグがあってそのせいで貴方に損害を与えたとしても、著作権者はいかなる責任も負いかねるのでその点を理解して使って欲しいのだ。

### ⚡ 利用制限事項・年齢制限

* 本アプリは **13歳以上** の方を対象としています。
  18歳未満の方は、必ず保護者または法定代理人の同意を得てください。
  **13歳未満の方は利用できません。**

* 以下の用途は禁止します：

  * 犯罪行為・法令違反
  * 他者を誹謗中傷したり、差別やハラスメントを助長する行為
  * わいせつ、過度に暴力的、または不快とされるコンテンツの生成依頼

* 本アプリは外部のAIサービスAPI（例: OpenAI, Anthropic, Google など）を利用しており、
  **各サービス提供元の利用規約が本アプリの利用に優先されます。**

* 開発者は、本アプリの利用によって生じたいかなる損害、損失、法的問題についても
  **一切の責任を負いません。**

**利用は自己責任でお願いします。**

## 💎 資料

- [VOICEVOXキャラクターリスト](doc/voicevox_speaker_list.md)
- [COEIROINKキャラクターリスト](doc/coeiroink_speaker_list.md)
- [炬燵で快適！VOICEVOXとZundaGPT2を別のPCで連携する方法](炬燵で快適！VOICEVOXとZundaGPT2を別のPCで連携する方法.md)
- [炬燵で快適！COEIROINKとZundaGPT2を別のPCで連携する方法](炬燵で快適！COEIROINKとZundaGPT2を別のPCで連携する方法.md)

<div class="page" />

## 💎 使用しているライブラリ

<details><summary>このアプリがお世話になってるOSSは以下の通りなのだ✨</summary>

### 🔖 pywebview 5.3.2

ホームページ： https://github.com/r0x0r/pywebview  
ライセンス：BSD-3-Clause license

### 🔖 openai 1.99.6

ホームページ： https://github.com/openai/openai-python  
ライセンス：Apache License 2.0

### 🔖 google-genai 1.21.1

ホームページ： https://github.com/googleapis/python-genai  
ライセンス：Apache License 2.0

### 🔖 anthropic 0.55.0

ホームページ： https://github.com/anthropics/anthropic-sdk-python  
ライセンス：MIT license

### 🔖 gTTS 2.5.1

ホームページ： https://github.com/pndurette/gTTS  
ライセンス：MIT License

### 🔖 requests 2.32.4

ホームページ： https://requests.readthedocs.io/en/latest/  
ライセンス：Apache License 2.0

### 🔖 PyAudio 0.2.14

ホームページ： https://people.csail.mit.edu/hubert/pyaudio/  
ライセンス：MIT License

### 🔖 pythonnet 3.0.3

ホームページ：https://github.com/pythonnet/pythonnet  
ライセンス：MIT License

### 🔖 langdetect 1.0.9

ホームページ：https://github.com/Mimino666/langdetect  
ライセンス：Apache License 2.0

### 🔖 pyperclip 1.9.0

ホームページ： https://github.com/asweigart/pyperclip
ライセンス：BSD 3-Clause "New" or "Revised" License

### 🔖 pydub 0.25.1

ホームページ：https://github.com/jiaaro/pydub  
ライセンス：MIT License

### 🔖 pywin32 306

ホームページ：https://github.com/mhammond/pywin32  
ライセンス：Python Software Foundation License (PSF)

### 🔖 MathJax 3.2.2

ホームページ： https://github.com/mathjax/MathJax  
ライセンス：Apache License 2.0

### 🔖 Highlight.js 11.9.0

ホームページ：https://github.com/highlightjs/highlight.js  
ライセンス：BSD-3-Clause license

### 🔖 Marked 12.0.0

ホームページ：https://github.com/markedjs/marked  
ライセンス：MIT license

### 🔖 mark.js 8.11.1

ホームページ：https://github.com/julkue/mark.js  
ライセンス：MIT license

### 🔖 Font Awesome Free 6.7.2

ホームページ：https://fontawesome.com/  
ライセンス：Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License

### 🔖 pyinstaller-versionfile

ホームページ：https://github.com/DudeNr33/pyinstaller-versionfile  
ライセンス：MIT license

### 🔖 PyInstaller 6.14.2
ホームページ： https://github.com/pyinstaller/pyinstaller  
ライセンス： GPL 2.0 License / Apache License 2.0  

</details>

<div class="page" />

## 💎 ライセンス

© 2024-2025 led-mirage

本アプリケーションは [MITライセンス](https://opensource.org/licenses/MIT) の下で公開されているのだ。詳細については、プロジェクトに含まれる LICENSE ファイルを参照して欲しいのだ。

<div class="page" />

## 💎 バージョン履歴

<details><summary>過去のバージョンアップの軌跡はこちらなのだ</summary>

### 1.29.0 (2025/09/07)

- キャラクター毎のカスタムスタイルを設定可能に。
  - 背景画像や文字色などを変更可能。
- スタイル（CSS）の調整
- その他バグ修正

### 1.28.0 (2025/08/31)

- カスタムCSSのサポート
  - custom.cssを配置することでスタイルの変更が可能に。

### 1.27.0 (2025/08/24)

- ローカルLLM（llama.cppなどのOpenAI互換API）に対応
  - settings.jsonのapi_base_urlにローカルLLMのURLを指定することでローカルLLMを使用可能に。

### 1.26.0 (2025/08/11)

- GPT-5シリーズに対応
  - gpt-5、gpt-5-miniモデルでストリーミング機能を使うにはOpenAIの`Verify Organization`必須となった。
  - そのため、組織認証をしていない場合は、ストリーミング機能を使わずに通信するようフォールバック処理を追加。
- openaiライブラリを1.99.6に更新

### 1.25.0 (2025/08/04)

- メッセージ入力テキストボックスの最大高を設定（制限以上になるとスクロールバーが出る）
- フランス語に対応

### 1.24.0 (2025/08/03)

- AIのメッセージ応答完了時に、メッセージ先頭にスクロールする処理を追加
- ビルドバッチ変更（毎回buildディレクトリを削除するように変更）

### 1.23.0 (2025/07/27)

- Raspberry Pi OS Bookwork 64bit に対応
- Linux Mint 22.1 Cinnamon Edition に対応

### 1.22.0 (2025/07/25)

- ダークモードの実装
  - appConfig.jsonファイルの "system"."theme" に `dark` または `light` を指定する
- PyInstallerのバージョンを6.14.2に更新

### 1.21.2 (2025/07/21)

- fix: OpenAI、Claudeの場合に`api_key_envvar`オプションが効かないバグを修正

### 1.21.1 (2025/07/13)

- クリップボードにテキストをコピーする処理をJS側からPython側に移設
  - `ZundaGPT2 Lite`の修正にあわせてこちらも修正

### 1.21.0 (2025/07/12)

- fix: 過去ログがロードできないバグを修正
- fix: f-Stringの書式を修正（Python 3.10-3.11に対応）

### 1.20.0 (2025/07/06)

- 会話履歴送信時に文字数上限を指定できる`history_char_limit`オプションを追加
  - `history_size`（履歴の最大件数）に加えて、合計文字数でも履歴送信を制御可能
  - `history_char_limit`が 0 の場合、文字数制限はなし
  - 文字数が上限を超えていても、過去3回分の会話は必ず送信される
- PyInstallerのバージョンを6.14.1に更新

### 1.19.0 (2025/06/26)

- チャット画面のストリーミング表示を改善
  - 受信中のメッセージもリアルタイムにマークダウンレンダリングするよう変更
    - 読みやすさ・見た目を向上
    - コードブロックは正しく閉じられるまでテキスト表示され、途中レンダリングによる崩れを防止
  - openaiライブラリを1.91.0に更新
  - anthropicライブラリを0.55.0に更新
  - google-genaiのバージョンを1.21.1に更新

### 1.18.0 (2025/06/17)

- AzureOpenAIで使用するAPIバージョンを`2025-04-01-preview`に更新
  - o4-miniなどの推論系のモデルに対応
- openaiライブラリを1.88.0に更新
- anthropicライブラリを0.54.0に更新

### 1.17.4 (2025/06/15)

- requestsライブラリを2.32.4に更新（CVE-2024-47081対応）

### 1.17.3 (2025/06/05)

- Fix: リプレイ時に空行は読み上げをスキップするように修正

### 1.17.2 (2025/06/04)

- Fix: Geminiを使用した場合、チャットの要約機能が動かないバグを修正
- キャラクター設定ファイルのAIモデルのデフォルト値を最近のモデルに変更

### 1.17.1 (2025/06/01)

- リリースモジュールのみの更新（機能の追加、変更はありません）
  - settingsフォルダ内の設定ファイルで設定されているAIモデルを最近のモデルに変更
  - 各EXEファイルのバージョンは1.17.0のまま変更はありません

### 1.17.0 (2025/05/31)

- アプリケーションログ出力機能追加
  - 設定ファイル（appConfig.json）に出力するログレベルの閾値を追加
  - 現在出力されるのは一部エラーのみ

### 1.16.4 (2025/05/30)

- リファクタリングのみ（機能の追加、変更はありません）
  - google gemini用のライブラリを`google-genai`に変更
    - `google-generativeai`ライブラリが Deprecated になったことによる措置
  - タイポ修正
    - appConfig.json中の`safty`を`safety`に修正
      - これによりGeminiのコンテンツフィルタの設定が初期されます
      - 設定を変更されていた方はお手数ですが再設定してください

### 1.16.3 (2025/05/24)

- リファクタリングのみ（機能の追加、変更はありません）
  - バックエンド側の構造整理
    - api/ … フロントとの橋渡しやルーティング処理
    - services/ … 各画面・機能ごとのロジック（サービス層）
    - config/ … 設定ファイル
    - utility/ … 共通関数、多言語処理などの補助的な処理
    - ステートクラスの導入、Windowクラスの導入
  - タイポ修正

### 1.16.2 (2025/05/18)

- リファクタリングのみ（機能の追加、変更はありません）
  - アプリケーション定数を別ファイルに分離
  - ビルドバッチの変更
  - PyInstallerのバージョンを6.13.0に更新

### 1.16.1 (2025/05/17)

- リファクタリングのみ（機能の追加、変更はありません）
  - View側にESMを導入して整理

### 1.16.0 (2025/05/11)

- アプリケーション設定ファイルにフォントファミリとフォントサイズの項目を追加
  - **font_family**: フォントの一覧（優先順）
  - **font_size**: フォントサイズ（px単位）
- Fix: 日本語の「」が重なって表示される問題を修正（CSSの修正）

### 1.15.0 (2025/05/04) 

- キャラクター設定ファイル（settings_xxx.json）に以下の項目を追加
  - **api_key_envvar**: APIキーを格納する環境変数名 
  - **api_endpoint_envvar**: APIエンドポイントを格納する環境変数名（AzureOpenAI Serviceにのみ影響）
- ドイツ語に対応
- openaiのバージョンを1.76.0に更新
- anthropicのバージョンを0.50.0に更新
- google-generativeaiのバージョンを0.8.5に更新
- PyInstallerのバージョンを6.12.0に更新
- タイポ修正

### 1.14.0 (2025/03/06)

- Claude 3.7 Sonnet の Extended Thinking（拡張思考モード）に対応
- モーダルダイアログのCSSのリファクタリング

### 1.13.0 (2025/02/19)

- OpenAI o1-preview、o1-miniモデルに対応
  - o1、o3-miniはティア制限のため未検証

### 1.12.0 (2025/02/18)

- チャットを要約する機能を追加
- チャット全体をクリップボードにコピーする機能を追加

### 1.11.1 (2025/02/13)

- Fix: ファイル横断検索画面でのHTMLエンコード抜けの修正
- Fix: プログラムコード部分や、ユーザーのメッセージ部分はMathJaxで数式に変換しないように修正

### 1.11.0 (2025/02/11)

- 設定切替画面で設定ファイルのグルーピングができるようにした

### 1.10.0 (2025/02/09)

- ファイル横断検索機能の実装
- デザインを一部変更
- フィンランド語とスペイン語に対応

### 1.9.0 (2025/02/06)

- メッセージをコピーするボタンを追加
- カスタムコンテキストメニューを追加して、選択したテキストをコピーできるようにした
- Fix: 設定ウィンドウをキャンセルしたときに、Welcomeメッセージが表示される問題を修正
- Fix: AIに再回答を依頼したときに、メッセージの順序がおかしくなる問題を修正

### 1.8.0 (2025/02/02)

- コードブロックにクリップボードにコピーするボタンを追加

### 1.7.0 (2025/01/26)

- 設定画面にチャット設定ファイルをオープンする機能を追加
- Fix: 文字列のエスケープ処理が抜けている個所を修正

### 1.6.2 (2025/01/25)

- Fix: 環境変数がセットされていないときのエラー処理を変更
- ZundaGPT2Liteに合わせるために、バージョン1.6.1は欠番

### 1.6.0 (2025/01/19)

- 言語サポート機能の追加（英語）
- Fix: index.htmlで使っているscriptタグにSRIハッシュを追加

### 1.5.0 (2025/01/04)

- チャットアイコンを表示する機能を追加

### 1.4.3 (2025/01/02)

- リプレイ機能（実験的機能）の実装… Ctrl + R でリプレイ開始
- Anthropic APIでエラーが発生したときのメッセージを分かりやすくした

### 1.4.2 (2025/01/01)

- コードブロック中にURLがあった場合に、不要な変換がおこなわれてしまう不具合を修正

### 1.4.1 (2024/12/30)

- appConfig.jsonの`voicevox_server`と`coeiroink_server`がプログラムに反映されないバグを修正

### 1.4.0 (2024/12/29)

- Anthropic社のAI、Claudeシリーズに対応
- チャット内容の表示を改善

### 1.3.0 (2024/12/07)

- 起動時に表示されるスプラッシュ画面を追加
- pywebviewのバージョンを5.3.2に更新
- openaiのバージョンを1.57.0に更新
- google-generativeaiのバージョンを0.8.3に更新

### 1.2.1 (2024/7/06)

- 回答表示処理中にブラウザでエラー（OUT OF MEMORYなど）が発生する場合がある問題に対処  
  parsedSentenceメソッド中のMathJax.typesetPromise()をコメントアウト

### 1.2.0 (2024/6/23)

- アプリケーションアイコンの追加
- 印刷する場合、codeブロックの中のテキストを右端で折り返すように修正

### 1.1.0 (2024/6/22)

- 印刷機能の追加
- 画面上部のボタンにツールチップを追加
- PyInstallerのバージョンを6.8.0に更新

### 1.0.1 (2024/6/8)

- openaiのバージョンを1.33.0に更新
- google-generativeaiのバージョンを0.6.0に更新
- requestsのバージョンを2.32.3に更新
- 再生環境による文末の音声途切れ問題を軽減するため、再生終了後に0.2秒間の待機時間を追加

### 1.0.0 (2024/6/2)

- Google Text-to-Speechに対応
- SAPI5に対応
- requestsのバージョンを2.32.2に更新
- バージョンを1.x.xに改定

### 0.11.0 (2024/5/19)

- Google Gemini APIに対応

### 0.10.0 (2024/4/29)

- Tex形式の行列式が正しく表示されない問題を解消

### 0.9.0 (2024/4/21)

- Readmeの使用しているライブラリ欄に、pywebviewの記載が洩れていたため追記
- openaiのバージョンを1.12.0から1.23.2に更新
- ChatAPIのタイムアウト値を設定ファイル（app_config.json）に持つように変更
- AIの回答中にあるURLが正しくリンク表示にならない問題に対処

### 0.8.0 (2024/4/6)

- メッセージ送信中止機能を追加
- Ctrl + F でテキストを検索する機能を追加（F3 or Shift + F3で候補移動）
- Welcomeメッセージの追加
- 設定ファイルのフォーマット変更（Welcome関連項目追加）
- Copyrightを動的に設定するように修正
- 英文が右端で折り返さない問題を修正

### 0.7.0 (2024/3/30)

- 再回答ボタンを追加
- チャットログが１つしかない場合に、そのログを削除できないバグを修正

### 0.6.0 (2024/3/23)

- メッセージの削除ボタンを追加
- PyInstallerの更新（6.4.0を使用）

### 0.5.1 (2024/3/16)

- 0.5.0で発生した数式が正しくレンダリングされないバグ（デグレード）を修正

### 0.5.0 (2024/3/9)

- マークダウン形式のテキストをHTMLに変換するように変更
- チャットリクエストがタイムアウトした際、リトライするかユーザーに選択してもらうように修正

### 0.4.0 (2024/3/3)

- 設定ファイルをappConfig.jsonとsettings.jsonに分離
- settings.jsonを配置するフォルダをsettingsフォルダに変更
- 設定の切り替えを行うUIを追加
- 画面左上に現在の設定のdisplay_nameを表示するように変更
- ウィンドウがフォーカスを失った後に再度戻ってくると、IMEの変換がうまくいかなくなる問題に対処
- チャットリクエスト時のタイムアウト処理を変更
- スピーカーのON/OFFを切り替えれるように変更
- ウィンドウサイズの初期値を設定ファイルで指定できるように変更
- その他、バグ修正、微調整など

### 0.3.0 (2024/2/23)

- 表示しているチャットのログファイル名をタイトルバーに表示するようにした
- 数式を左寄せ表示するように修正
- 発声時のエラー処理を修正

### 0.2.0 (2024/2/18)

- ログに記録した以前のチャットに移動する機能を追加（prev、next）
- 新しいチャットを開始している機能を追加（new）
- チャットを削除する機能を追加
- TeX形式の数式を表示する機能を追加
- ログファイルの形式を変更
- チャットリクエスト時のタイムアウト処理の追加
- その他バグ修正など

### 0.1.1 (2024/2/13)
 
- ソース添付のsettings.jsonを変更。プログラムに変更なし。

### 0.1.0 (2024/2/12)
 
- ファーストリリース

</details>
