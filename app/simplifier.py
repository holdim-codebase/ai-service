import os
import openai
import json
import sys

sys.path.append("../modules/sequence_generator.py")

from modules.sequence_generator import SimplifierModel

openai.api_key = "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"


class Simplifier():

    def load_model_config(self, mode):
        return SimplifierModel(json.load(open(f'modules/configs/{mode}.json')))

    def response(self, text, temperature_response, top_p, max_tokens, mode):
        seq_model = self.load_model_config(mode)
        answer = seq_model.response(text, temperature_response, top_p, max_tokens)
        print(answer)
        return answer
