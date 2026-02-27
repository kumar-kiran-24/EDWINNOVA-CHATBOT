import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


from src.data_retriver import Dataretriver
from src.chatbot import ChatBot


app=FastAPI()

class ChatRequest(BaseModel):
    question:str


chatbot=ChatBot()
data_retriver=Dataretriver()

@app.post("/chat")
async def chat(request:ChatRequest):
    question=request.question
    context=data_retriver.search_data(query=question)
    resopnse=chatbot.chatbot(question=question,context=context,session_id="1")
    print(resopnse)

    return {"Response":resopnse}


