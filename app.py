from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
client = OpenAI()

class Chat(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: Chat):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":"You are an AI assistant helping a Herbalife distributor manage team and create marketing content."},
            {"role":"user","content":data.message}
        ]
    )

    return {"reply": response.choices[0].message.content}

from fastapi.responses import FileResponse

@app.get("/")
def home():
    return FileResponse("index.html")
