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

    def control_broken_response(self, answer):
        splitted_answer = re.split("(?<=[.!?]) +", answer)
        if splitted_answer[-1][-1] not in ('.', '?', '!'):
            corrected_answer = ' '.join(splitted_answer[0:-1])
            if corrected_answer == '' and corrected_answer != answer: corrected_answer = 'Sorry, I cut off the whole thing because the answer was too short...'
        return corrected_answer

    def response(self, text, temperature_response, top_p, max_tokens, mode, regen, cut_off):
        seq_model = self.load_model_config(mode)
        answer = ''
        for i in range(regen + 1):
            print(i)
            answer = seq_model.response(text, temperature_response, top_p, max_tokens)
            print('Answer1: ', answer)
            if answer[-1] in ('.', '?', '!'): break
        print('Answer2: ', answer)
        if cut_off: answer = self.control_broken_response(answer)
        print('Answer3: ', answer)
        return answer
