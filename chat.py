from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from prompt import createPrompt
from langchain.memory import ChatMessageHistory
from translator import DeepL
import os


os.environ['TRANSFORMERS_CACHE'] = "/data1/ysc/tmp"
os.environ['HF_HOME'] = "/data1/ysc/tmp"

class MedChat:
    def __init__(self, llm="llama3:70b-instruct", translator=None, max_q=10, prompt=None):
        self.llm = ChatOllama(model=llm)  # ChatOllama 언어 모델 초기화
        self.output_parser = StrOutputParser()
        self.history = ChatMessageHistory()
        self.max_q = max_q
        self.ext_data = ""
        self.query_number = 0
        
        if translator == "deepL":
            self.translator = DeepL()
        elif translator == None:
            self.translator = None
            
        prompt, prompt_request_diagnosis = createPrompt(prompt_type=prompt)
        self.chain = prompt | self.llm | self.output_parser
        self.chain_request_diagnosis = prompt_request_diagnosis | self.llm | self.output_parser
            
    
    def __call__(self, message):
        self.query_number += 1
        
        print(f"{message}")
        if self.translator != None:
            message = self.translator(source_lang="KO", target_lang="EN", message=message)
            print(f"{message}")
            
        if self.max_q != None and self.query_number >= self.max_q:
            output = self.chain_request_diagnosis.invoke({
                'input': message, 
                'history': self.history.messages
            })
        else:
            output = self.chain.invoke({
                'input': message, 
                'history': self.history.messages
            })
            
        print(f"{output}")
        if self.translator != None:
            output = self.translator(source_lang="EN", target_lang="KO", message=output)
            print(f"{output}")
        
        self.history.add_user_message(message)
        return output