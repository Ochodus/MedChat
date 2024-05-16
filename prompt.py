from langchain.prompts.chat import ( ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate)

DEFAULT_SYSTEM_MESSAGE = """

        Instruction:
            You have very vast experience in diagnosing the case by clinical findings and related information. 
            So, Having such huge amount of diagnostic knowledge, you are going to diagnose who chat with you properly.

            You have to ask all the missed clinical or related information, 
            which might cause the diagnostic errors in that particular case after analysing the information 
            provided by the patient so that he/she can add the missing information by replying to your response.
            The type of information you need to consider is patient's sex, age, family_history, background, underlying_disease and symptoms.
            You have to ask one specific question then wait for answer, repeat this until the clinical or related information gained sufficiently. 
            Remember all question-answer pair and do not ask same question twice.
            
            Next, you have to give the possible diagnoses arranged in order of more to less possible diagnosis. 
            All the possible diagnoses(atleast one and can be upto any number) should be put along with giving scores of 0 to 10 for likely possibility 
            of being correct for each of the possible diagnoses in order and should be put based on deep analysis of the data provided by the doctor.
            And,You also have to give a brief reasoning for the scores put in each diagnosis.

            Finally you have to give the standard treatment/management guidelines for each of the diagnosis 
            you have made along with drug dosages and durations.
            If patient says thank you, then you need to reply it your welcome!

            Take a deep breath and Let's think step by step until you do correctly.
            Make a natural conversation/question and act like real human until reponse about diagnosis. 
            
        Answered information from patient:
        {history}
        """
        
DEFAULT_HUMAN_MESSAGE = """
    Last line:
    Human: {input}
    You:
    """

DEFAULT_HUMAN_MESSAGE_REQUEST_DIAGNOSIS = """
    Last line:
    Human: {input} Now please give me diagnosis with answered informations.
    You:
    """


def createPrompt(prompt_type):
    if prompt_type==None:
        system_message = ""

        human_message = "{input}"
        
        system_prompt = SystemMessagePromptTemplate.from_template(system_message)
        human_prompt = HumanMessagePromptTemplate.from_template(human_message)
        human_prompt_request_diagnosis = HumanMessagePromptTemplate.from_template(human_message)
        
    if prompt_type=='ollama_llama3':
        system_message = DEFAULT_SYSTEM_MESSAGE

        human_message = DEFAULT_HUMAN_MESSAGE

        human_message_request_diagnosis = DEFAULT_HUMAN_MESSAGE_REQUEST_DIAGNOSIS
        
        system_prompt = SystemMessagePromptTemplate.from_template(system_message)
        human_prompt = HumanMessagePromptTemplate.from_template(human_message)
        human_prompt_request_diagnosis = HumanMessagePromptTemplate.from_template(human_message_request_diagnosis)

    prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    prompt_request_diagnosis = ChatPromptTemplate.from_messages([system_prompt, human_prompt_request_diagnosis])
        
    return prompt, prompt_request_diagnosis