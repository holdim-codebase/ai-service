import os
import openai
import json
import sys
import re

sys.path.append("../modules/sequence_generator.py")

from modules.sequence_generator import SimplifierModel

openai.api_key = "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"


class Simplifier():

    def load_model_config(self, mode):
        return SimplifierModel(json.load(open(f'modules/configs/{mode}.json')))

    def control_broken_response(self, response):
        splitted_response = re.split("(?<=[.!?]) +", response)
        if splitted_response[-1][-1] not in ('.', '?', '!'):
            corrected_response = ' '.join(splitted_response[0:-1])
            return corrected_response if corrected_response != '' and corrected_response != response else 'Sorry, I cut off the whole thing because the answer was too short...'
        return response

    def response(self, text, temperature_response, top_p, max_tokens, mode, regen, cut_off):
        seq_model = self.load_model_config(mode)
        answer = ''
        for i in range(regen + 1):
            answer = seq_model.response(text, temperature_response, top_p, max_tokens)
            if answer[-1] in ('.', '?', '!'): break
        if cut_off: answer = self.control_broken_response(answer)
        print(answer)
        return answer
