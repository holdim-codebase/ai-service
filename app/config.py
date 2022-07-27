from dotenv import load_dotenv
import os

load_dotenv()

SIMPLIFIER_PARMS = {"REGEN": 0,
                    "CUT_OFF": True,
                    "TEMPERATURE": float(os.getenv('CONFIG_TEMPERATURE', 0.87)),
                    "MAX_TOKENS": int(os.getenv('MAX_TOKENS', 250)),
                    "MODEL": os.getenv('MODEL', "text-davinci-002"),
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
