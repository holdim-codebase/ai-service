from openai import Completion
import os

path = os.path.dirname(__file__)


class SimplifierModel():
    def __init__(self, config=None):
        self.config = config

    def response(self, text, temperature_response, top_p, max_tokens):
        res = Completion.create(
            model=self.config['model'],
            prompt=self.generate_prompt(text),
            temperature=temperature_response,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        return res['choices'][0]['text'].lstrip()

    def response_from_config(self, text, temperature=0.7, key='1111'):
        res = Completion.create(
            model=self.config['model'],
            prompt=self.generate_prompt(text),
            temperature=temperature,
            max_tokens=int(self.config['max_tokens']),
            frequency_penalty=float(self.config['frequency_penalty']),
            presence_penalty=float(self.config['presence_penalty']),
            user=key)
        return res['choices'][0]['text'].lstrip()

    def generate_prompt(self, text, to_print=True):
        if to_print: print(f"{self.config['completion_setup']}{text}\n\n{self.config['task']}")
        return f"{self.config['completion_setup']}{text}\n\n{self.config['task']}"
