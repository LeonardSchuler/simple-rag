import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Annotated

from .models import Message, Document
from . import dependencies as deps
from ..core import ports


app = FastAPI()
templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/message")
async def send_message(
    message: Message,
    message_service: Annotated[ports.MessageService, Depends(deps.get_message_service)],
):
    response = message_service.process(message.message)
    return JSONResponse({"response": response})


def main():
    """CLI entry point to run the FastAPI app using Uvicorn."""
    uvicorn.run("rag.app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
