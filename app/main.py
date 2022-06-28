from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pathlib import Path
from simplifier import Simplifier
import uvicorn as uvicorn
from fastapi.templating import Jinja2Templates
import json

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=Path(BASE_PATH, 'templates'))

app = FastAPI(
    title="AI simplifier"
)
simplifier = Simplifier()


@app.post("/post")
def chatbot_response(
        user_message: str = Form(...),
        temperature_response: float = Form(...),
        top_p: float = Form(...),
        max_tokens: int = Form(...),
):
    response = simplifier.response(user_message, temperature_response, top_p, max_tokens)
    return json.dumps(response)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", context={'request': request})


if __name__ == "__main__":
    # documentation:
    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/redoc

    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
