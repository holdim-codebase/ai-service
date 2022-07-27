import openai
import sys
import re
from config import SIMPLIFIER_PARMS
from openai import Completion

sys.path.append("./config.py")
openai.api_key = SIMPLIFIER_PARMS['OPENAI_API_KEY']


class Simplifier():
    def __init__(self):
        self.config = SIMPLIFIER_PARMS

    def generate_prompt(self, text, to_print=True):
        prompt = f"{self.config['COMPLETION_SETUP']}{text}\n\n{self.config['TASK']}"
        if to_print: print(prompt)
        return prompt

    def generate_GPT3_sequence(self, text, key='1111'):
        res = Completion.create(
            model=self.config['MODEL'],
            prompt=self.generate_prompt(text),
            temperature=self.config['TEMPERATURE'],
            max_tokens=self.config['MAX_TOKENS'],
            frequency_penalty=float(self.config['FREQUENCY_PENALTY']),
            presence_penalty=float(self.config['PRESENCE_PENALTY']),
            user=key)
        return res['choices'][0]['text'].lstrip()

    def control_broken_response(self, response):
        splitted_response = re.split("(?<=[.!?]) +", response)
        if splitted_response[-1][-1] not in ('.', '?', '!'):
            corrected_response = ' '.join(splitted_response[0:-1])
            return corrected_response if corrected_response != '' and corrected_response != response else 'Sorry, I cut off the whole thing because the answer was too short...'
        return response

    def generate_answer(self, text):
        answer = ''
        for i in range(self.config['REGEN'] + 1):
            answer = self.generate_GPT3_sequence(text)
            if answer[-1] in ('.', '?', '!'): break
        if self.config['CUT_OFF']: answer = self.control_broken_response(answer)
        print(answer)
        return answer
