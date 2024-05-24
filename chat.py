import os
from langchain_community.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama
from prompt import createPrompt
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ChatMessageHistory
from translator import DeepL

os.environ['HF_HOME'] = "/data1/wooshin/tmp"

class MedChat:
    def __init__(self, llm="llama3:70b-instruct", translator=None, max_q=10, prompt=None, logger=None, embedding_model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.llm = ChatOllama(model=llm)  # ChatOllama 언어 모델 초기화
        self.output_parser = StrOutputParser()
        self.history = ChatMessageHistory()
        self.max_q = max_q
        self.ext_data = ""
        self.query_number = 0
        

        if translator == "deepL":
            self.translator = DeepL()
        elif translator is None:
            self.translator = None

        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.vectorstore = None

        prompt, prompt_request_diagnosis = createPrompt(prompt_type=prompt)
        self.chain = prompt | self.llm | self.output_parser
        self.chain_request_diagnosis = prompt_request_diagnosis | self.llm | self.output_parser

        self.logger = logger

    def process_user_query(self, query):
        self.model_name = 'pritamdeka/S-PubMedBert-MS-MARCO'
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.model_name)

        self.medvector_db = FAISS.load_local('./med_vectorstore', self.embedding_model, allow_dangerous_deserialization=True)
        docs = self.medvector_db.similarity_search(query)

        return docs

    def _logging_chat_history(self, talker, message):
        if self.logger:
            self.logger.info(f"{talker}: {message}")

    def reset(self, logger=None):
        self.history.clear()
        self.query_number = 0
        self.logger = logger

    def __call__(self, message):
        self.query_number += 1

        self._logging_chat_history("Patient", message)
        if self.translator:
            message = self.translator(source_lang="KO", target_lang="EN", message=message)
        
        # import ipdb; ipdb.set_trace()
        query_history = [query.content for query in self.history.messages]
        query_history.append(message)

        rag_result = self.process_user_query(' '.join(query_history))

        print(rag_result)

        if self.max_q is not None and self.query_number >= self.max_q:
            output = self.chain_request_diagnosis.invoke({
                'input': message,
                'history': self.history.messages,
                'rag': rag_result
            })
        else:
            output = self.chain.invoke({
                'input': message,
                'history': self.history.messages,
                'rag': rag_result
            })

        if self.translator:
            output = self.translator(source_lang="EN", target_lang="KO", message=output)

        self._logging_chat_history("Med Chat", output)

        self.history.add_user_message(message)
        return output