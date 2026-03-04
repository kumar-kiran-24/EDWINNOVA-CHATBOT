import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.data_retriver import Dataretriver
from src.chatbot import ChatBot

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] , 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    session_id: str

chatbot = ChatBot()
data_retriver = Dataretriver()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        question = request.question
        session_id = request.session_id

        context = data_retriver.search_data(query=question)

        response = chatbot.chatbot(
            question=question,
            context=context,
            session_id=session_id
        )

        return {"Response": response}

    except Exception as e:
        return {"error": str(e)}
@app.get("/")
def health():
    return {"status":"running"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)