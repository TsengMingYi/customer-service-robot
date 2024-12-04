#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/11 1:57 上午
@Author : www.mingerzeng@gmail.com
@File : app_handler.py
"""
from dataclasses import dataclass
import uuid
from operator import itemgetter
from typing import Dict, Any
from uuid import UUID
from injector import inject
from langchain_core.memory import BaseMemory
from langchain_core.tracers import Run

from internal.schema.app_schema import CompletionReq
from pkg.response import success_json,validate_error_json,success_message
from internal.exception import FailException
from internal.service import VectorDatabaseService, VectorDatabaseService1
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.output_parsers import StrOutputParser

@inject
@dataclass
class AppHandler:
    """應用控制器"""
    vector_database_service: VectorDatabaseService
    vector_database_service1: VectorDatabaseService1


    # @classmethod
    # def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
    #     """加載記憶變量資訊"""
    #     # 1. 從config中獲取configurable
    #     configurable = config.get("configurable", {})
    #     configurable_memory = configurable.get("memory", None)
    #     if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
    #         return configurable_memory.load_memory_variables(input)
    #     return {"history": []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        # """存儲對應的上下文資訊到記憶實體中"""
        # configurable = config.get("configurable", {})
        # configurable_memory = configurable.get("memory", None)
        # if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
        #     configurable_memory.save_context(run_obj.inputs, run_obj.outputs)
        pass

    def debug(self,app_id: UUID):
        """聊天接口"""
        # 1. 提取從接口中獲取的輸入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2. 創建prompt與記憶
        # 若是詢問有關於機械雲產品資料請要求使用者登入
        system_prompt = """你是一個強大的工研院智慧機械雲客服機器人，能根據對應的上下文和歷史對話信息回覆用戶問題。回答問題請註意以下三點：
        1.只回答跟工研院有關或是跟智慧機械雲有關的問題。
        2.除了不要回答關於「如何解除安裝智慧機械雲APP」這個問題。
        3.若是詢問有關於機械雲產品資料請要求使用者登入。
        \n\n<context>{context}</context>"""
        prompt = ChatPromptTemplate.from_messages([
            ("system",system_prompt),
            # MessagesPlaceholder("history"),
            ("human","{query}"),
        ])
        # memory = ConversationBufferWindowMemory(
        #     k=3,
        #     input_key="query",
        #     output_key="output",
        #     return_messages=True,
        #     # chat_memory = FileChatMessageHistory("/var/app/current/storage/memory/chat_history.txt"),
        #     # chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
        # )

        # 3. 創建llm
        llm = ChatOpenAI(model="gpt-4o-mini",api_key="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")

        # 4. 創建鏈應用
        # retriever = self.vector_database_service.get_retriever() | self.vector_database_service.combine_documents
        # chain = (RunnablePassthrough.assign(
        #     history=RunnableLambda(self._load_memory_variables) | itemgetter("history"),
        #     context=itemgetter("query") | retriever
        # ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        # # 5. 調用鏈生成內容
        # chain_input = {"query": req.query.data}
        # content = chain.invoke(chain_input, config={"configurable":{"memory":memory}})

        retriever = self.vector_database_service.get_retriever() | self.vector_database_service.combine_documents
        chain = (
            RunnablePassthrough.assign(
                context=itemgetter("query") | retriever
            ) | prompt | llm | StrOutputParser()
        ).with_listeners(on_end=self._save_context)

        # 4. 調用鏈生成內容
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input)
        # # 2. 構建組件
        # prompt = ChatPromptTemplate.from_template("{query}")
        # llm = ChatOpenAI(model="gpt-4o-mini")
        # parser = StrOutputParser()
        #
        # # 3. 構建鏈
        # chain = prompt | llm | parser
        #
        # # 4. 調用鏈得到結果
        # content = chain.invoke({"query": req.query.data})

        # # 2. 構建Openai客戶端，並發起請求
        # llm = ChatOpenAI(model="gpt-4o-mini")
        # # client = OpenAI()
        #
        # # 3. 得到請求響應，然後將Openai的響應傳遞給前端
        # ai_message = llm.invoke(prompt.invoke({"query":req.query.data}))
        #
        # parser = StrOutputParser()

        # # 4. 解析響應內容
        # content = parser.invoke(ai_message)
        # completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role":"system","content":"你是openai開發的聊天機器人，請根據用戶的輸入回覆對應的信息"},
        #         {"role":"user","content": req.query.data}
        #     ]
        # )

        # content = completion.choices[0].message.content

        return success_json({"content":content})
    

    def member(self,app_id: UUID):
        """聊天接口"""
        # 1. 提取從接口中獲取的輸入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2. 創建prompt與記憶
        system_prompt = "你是一個強大的工研院智慧機械雲客服機器人，能根據對應的上下文和歷史對話信息回覆用戶問題。只回答跟工研院有關或是跟智慧機械雲有關的問題，除了不要回答關於「如何解除安裝智慧機械雲APP」這個問題。 \n\n<context>{context}</context>"
        prompt = ChatPromptTemplate.from_messages([
            ("system",system_prompt),
            # MessagesPlaceholder("history"),
            ("human","{query}"),
        ])
        # memory = ConversationBufferWindowMemory(
        #     k=3,
        #     input_key="query",
        #     output_key="output",
        #     return_messages=True,
        #     # chat_memory = FileChatMessageHistory("/var/app/current/storage/memory/chat_history1.txt"),
        #     # chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
        # )

        # 3. 創建llm
        llm = ChatOpenAI(model="gpt-4o-mini",api_key="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")

        # 4. 創建鏈應用
        # retriever = self.vector_database_service1.get_retriever() | self.vector_database_service1.combine_documents
        # chain = (RunnablePassthrough.assign(
        #     history=RunnableLambda(self._load_memory_variables) | itemgetter("history"),
        #     context=itemgetter("query") | retriever
        # ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        # # 5. 調用鏈生成內容
        # chain_input = {"query": req.query.data}
        # content = chain.invoke(chain_input, config={"configurable":{"memory":memory}})

        retriever = self.vector_database_service1.get_retriever() | self.vector_database_service1.combine_documents
        chain = (
            RunnablePassthrough.assign(
                context=itemgetter("query") | retriever
            ) | prompt | llm | StrOutputParser()
        ).with_listeners(on_end=self._save_context)

        # 4. 調用鏈生成內容
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input)
        # # 2. 構建組件
        # prompt = ChatPromptTemplate.from_template("{query}")
        # llm = ChatOpenAI(model="gpt-4o-mini")
        # parser = StrOutputParser()
        #
        # # 3. 構建鏈
        # chain = prompt | llm | parser
        #
        # # 4. 調用鏈得到結果
        # content = chain.invoke({"query": req.query.data})

        # # 2. 構建Openai客戶端，並發起請求
        # llm = ChatOpenAI(model="gpt-4o-mini")
        # # client = OpenAI()
        #
        # # 3. 得到請求響應，然後將Openai的響應傳遞給前端
        # ai_message = llm.invoke(prompt.invoke({"query":req.query.data}))
        #
        # parser = StrOutputParser()

        # # 4. 解析響應內容
        # content = parser.invoke(ai_message)
        # completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role":"system","content":"你是openai開發的聊天機器人，請根據用戶的輸入回覆對應的信息"},
        #         {"role":"user","content": req.query.data}
        #     ]
        # )

        # content = completion.choices[0].message.content

        return success_json({"content":content})

    # def ping(self):
    #     return self.api_tool_service.api_tool_invoke()
        # return success_json()
        # raise FailException("資料未找到")
        # return {"ping": "pong"}
