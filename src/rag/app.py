from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from . import llm, db
from .models import Message


app = FastAPI()
templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/message")
async def send_message(message: Message):
    # Simple “AI” response logic
    text_embedding = db.get_embeddings(message.text)
    docs_embedded = db.search_similar(text_embedding)
    docs = db.inverse_embeddings(docs_embedded)
    response = llm.answer(message.text, docs)

    return JSONResponse({"response": response})
