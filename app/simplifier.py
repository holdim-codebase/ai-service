import os
import openai
import json
import sys

sys.path.append("../modules/sequence_generator.py")

from modules.sequence_generator import SimplifierModel

openai.api_key = os.environ.get("OPENAI_API_KEY")


class Simplifier():

    def load_model_config(self):
        return SimplifierModel(json.load(open('modules/configs/ETS.json')))

    def response(self, text, temperature_response, top_p, max_tokens):
        seq_model = self.load_model_config()
        answer = seq_model.response(text, temperature_response, top_p, max_tokens)
        return answer
