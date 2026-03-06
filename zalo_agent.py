import os
import requests
from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

ZALO_TOKEN = "YOUR_ZALO_OA_TOKEN"

def ask_ai(message):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant helping a Herbalife leader manage her team."},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content


@app.post("/webhook")

async def webhook(req: Request):

    data = await req.json()

    user_message = data["message"]["text"]
    user_id = data["sender"]["id"]

    ai_reply = ask_ai(user_message)

    send_to_zalo(user_id, ai_reply)

    return {"status": "ok"}


def send_to_zalo(user_id, text):

    url = "https://openapi.zalo.me/v3.0/oa/message/cs"

    headers = {
        "access_token": ZALO_TOKEN
    }

    payload = {
        "recipient": {"user_id": user_id},
        "message": {"text": text}
    }

    requests.post(url, json=payload, headers=headers)
