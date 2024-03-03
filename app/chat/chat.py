# ZundaGPT2
#
# チャットクラス
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import os
import httpx
from datetime import datetime
from typing import Callable

from openai import OpenAI
from openai import AzureOpenAI
from openai import APITimeoutError, AuthenticationError, NotFoundError

# チャット基底クラス
class Chat:
    # コンストラクタ
    def __init__(self, client, model: str, instruction: str, bad_response: str, history_size: int):
        self.messages = []
        self.client = client
        self.model = model
        self.instruction = instruction
        self.bad_response = bad_response
        self.history_size = history_size
        self.chat_start_time = datetime.now()
        self.chat_update_time = datetime.now()

    # メッセージを送信して回答を得る
    def send_message(
        self,
        text: str,
        recieve_chunk: Callable[[str], None],
        recieve_sentence: Callable[[str], None],
        end_response: Callable[[str], None],
        on_error: Callable[[Exception, str], None]) -> str:

        try:
            self.messages.append({"role": "user", "content": text})
            messages = self.messages[-self.history_size:]
            messages.insert(0, {"role": "system", "content": self.instruction})
            stream = self.client.chat.completions.create(model=self.model, messages=messages, stream=True)

            content = ""
            sentence = ""
            role = ""
            for chunk in stream:
                if chunk.choices[0].delta.role is not None:
                    role = chunk.choices[0].delta.role

                if chunk.choices[0].delta.content is not None:
                    chunk_content = chunk.choices[0].delta.content

                    content += chunk_content
                    sentence += chunk_content
                    recieve_chunk(chunk_content)

                    if sentence.endswith(("。", "\n", "？", "！")):
                        recieve_sentence(sentence)
                        sentence = ""

            if sentence != "":
                recieve_sentence(sentence)

            if content:
                self.messages.append({"role": role, "content": content})
                self.chat_update_time = datetime.now()
                end_response(content)
                return content
            else:
                end_response(self.bad_response)
                return self.bad_response
        except AuthenticationError as e:
            on_error(e, "Authentication")
        except (APITimeoutError, TimeoutError) as e:
            on_error(e, "Timeout")
        except NotFoundError as e:
            on_error(e, "EndPointNotFound")
        except Exception as e:
            on_error(e, "Exception")
        
# OpenAI チャットクラス
class ChatOpenAI(Chat):
    def __init__(self, model: str, instruction: str, bad_response: str, history_size: int):
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("環境変数 OPENAI_API_KEY が設定されていません。")

        client = OpenAI(timeout=httpx.Timeout(15.0, connect=5.0))
        super().__init__(
            client = client,
            model = model,
            instruction = instruction,
            bad_response = bad_response,
            history_size = history_size
        )

# Azure OpenAI チャットクラス
class ChatAzureOpenAI(Chat):
    def __init__(self, model: str, instruction: str, bad_response: str, history_size: int):
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        if endpoint is None:
            raise ValueError("環境変数 AZURE_OPENAI_ENDPOINT が設定されていません。")

        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("環境変数 AZURE_OPENAI_API_KEY が設定されていません。")

        client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2023-05-15", timeout=httpx.Timeout(15.0, connect=5.0))
        super().__init__(
            client = client,
            model = model,
            instruction = instruction,
            bad_response = bad_response,
            history_size = history_size
        )

# チャットファクトリー
class ChatFactory:
    # api_idに基づいてChatオブジェクトを作成する
    @staticmethod
    def create(api_id: str, model: str, instruction: str, bad_response: str, history_size: int) -> Chat:
        if api_id == "OpenAI":
            return ChatOpenAI(model, instruction, bad_response, history_size)
        elif api_id == "AzureOpenAI":
            return ChatAzureOpenAI(model, instruction, bad_response, history_size)
        else:
            raise ValueError("API IDが間違っています。")
