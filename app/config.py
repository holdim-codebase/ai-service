from dotenv import load_dotenv
import os

load_dotenv()


def set_conf(completion_setup, task):
    return {'COMPLETION_SETUP': completion_setup, 'TASK': task}


CONTEXT_PARAMS = {'default':
                      set_conf('My second grader asked me what this passage means:\n',
                               'I understood the text and explained what the proposal is about:\n'),
                  'ETS':
                      set_conf('My second grader asked me what this passage means:\n',
                               'I rephrased it for him, in plain language a second grader can understand:\n'),
                  'TLDR':
                      set_conf('',
                               'TL;DR:\n'),
                  'terms':
                      set_conf('',
                               'Explain all the crypto terms from proposal above a second grader can understand, each from a new line:\n'),
                  'empty':
                      set_conf('',
                               '')
                  }
CONTEXT_PARAMS_NAMES = list(CONTEXT_PARAMS.keys())
SIMPLIFIER_PARMS = {"REGEN": 0,
                    "CUT_OFF": True,
                    "TEMPERATURE": float(os.getenv('CONFIG_TEMPERATURE', 0.87)),
                    "MAX_TOKENS": int(os.getenv('MAX_TOKENS', 250)),
                    "MODEL": os.getenv('MODEL', "text-davinci-003"),
                    "PORT": int(os.getenv('PORT', 8080)),
                    "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY', ''),
                    "COMPLETION_SETUP": "My second grader asked me what this passage means:\n",
                    "TASK": "I understood the text and explained what the proposal is about:\n",
                    "STOP": ["\n"],
                    "FREQUENCY_PENALTY": 1,
                    "PRESENCE_PENALTY": 1,
                    "TOP_P": 1,
                    "TOPIC_PATH": 'projects/holdim/topics/ai-updater'
                    }
