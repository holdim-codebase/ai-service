from fastapi import FastAPI, Request
from pathlib import Path
from simplifier import Simplifier
import uvicorn as uvicorn
import json
import base64
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import sys
from config import SIMPLIFIER_PARMS, CONTEXT_PARAMS_NAMES
import os

BASE_PATH = Path(__file__).resolve().parent
sys.path.append("./config.py")

NON_SUMMARIZATION_THRESHOLD = 250
GPT3_SUMMARIZATION_THRESHOLD = 9200
GPT3_VERSION = 3
GPT4_VERSION = 4

app = FastAPI(
    title="AI simplifier"
)
simplifier = Simplifier()
publisher = pubsub_v1.PublisherClient()
load_dotenv()
topic_path = SIMPLIFIER_PARMS["TOPIC_PATH"]
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if os.getenv('OPENAI_API_KEY') == '':
    raise Exception('OpenAPI_Key', 'Set OPENAI_API_KEY environment variable')


def control_config_name(config_name):
    if config_name == '':
        return 'default'
    elif config_name in CONTEXT_PARAMS_NAMES:
        return config_name
    else:
        print(CONTEXT_PARAMS_NAMES, config_name)
        raise Exception("Enter a correct config name.")


@app.post("/")
async def chatbot_response(info: Request):
    req_info = await info.json()
    data = req_info['message']['data']
    message_bytes = base64.b64decode(data)
    message = message_bytes.decode('utf-8')
    user_message = json.loads(message)
    config_name = user_message['configName']
    config_name = control_config_name(config_name)
    senior_text = user_message['seniorText']
    metadata = user_message['metadata']
    junior_text = ""
    set_issue_number = False  # Automatically publish proposal to app: default False

    if len(senior_text) < NON_SUMMARIZATION_THRESHOLD:
        junior_text = "Proposal is too SHORT"
    else:
        try:
            if len(senior_text) < GPT3_SUMMARIZATION_THRESHOLD:
                junior_text = simplifier.generate_answer(senior_text, config_name, GPT3_VERSION)
            else:
                junior_text = simplifier.generate_answer(senior_text, config_name, GPT4_VERSION)
            set_issue_number = True
        except Exception as e:
            if "maximum context length is" in str(e):
                junior_text = "Proposal is too long"
            else:
                raise e

    json_final = json.dumps({'juniorText': junior_text, 'configName': config_name, 'metadata': metadata,
                             'setIssueNumber': set_issue_number}).encode("utf-8")
    future = publisher.publish(topic_path, json_final)
    print(f'published message id {future.result()}')
    return json.dumps({})


if __name__ == "__main__":
    # documentation:
    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/redoc

    uvicorn.run("main:app", host="0.0.0.0", port=SIMPLIFIER_PARMS['PORT'], log_level="info")
