import requests

class DeepL:
    def __init__(self, url_for_deepl='https://api-free.deepl.com/v2/translate'):
        self.url_for_deepl = url_for_deepl
        self.auth_key = input('Enter your deepL API key: ')
        
    def __call__(self, source_lang, target_lang, message):
        params = {'auth_key' : self.auth_key, 'text' : message, 'source_lang' : source_lang, "target_lang": target_lang }
        result = requests.post(self.url_for_deepl, data=params, verify=False)
        return result.json()['translations'][0]["text"]