from fastapi import FastAPI, Request
from pathlib import Path
from simplifier import Simplifier
import uvicorn as uvicorn
import json
import base64
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import sys
from config import SIMPLIFIER_PARMS
import os

BASE_PATH = Path(__file__).resolve().parent
sys.path.append("./config.py")

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


@app.post("/")
async def chatbot_response(info: Request):
    req_info = await info.json()
    data = req_info['message']['data']
    message_bytes = base64.b64decode(data)
    message = message_bytes.decode('utf-8')
    user_message = json.loads(message)
    juniorDescription = simplifier.generate_answer(user_message['seniorDescription'])
    id = user_message['id']
    json_final = json.dumps({id: id, juniorDescription: juniorDescription}).encode("utf-8")
    future = publisher.publish(topic_path, json_final)
    print(f'published message id {future.result()}')
    return json.dumps({})


if __name__ == "__main__":
    # documentation:
    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/redoc

    uvicorn.run("main:app", host="0.0.0.0", port=SIMPLIFIER_PARMS['PORT'], log_level="info")
