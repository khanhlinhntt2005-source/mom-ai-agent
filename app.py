from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import re

app = FastAPI()
client = OpenAI()

scheduler = BackgroundScheduler()
scheduler.start()

reminders = []

class Chat(BaseModel):
    message: str


# ---------- REMINDER TOOL ----------

def create_reminder(text, time_str):

    run_time = datetime.fromisoformat(time_str)

    def remind():
        print("REMINDER:", text)

    scheduler.add_job(remind, trigger="date", run_date=run_time)

    reminders.append({
        "text": text,
        "time": time_str
    })


# ---------- POSTER TOOL ----------

def generate_poster(prompt):

    img = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    return img.data[0].url


# ---------- AI CHAT ----------

@app.post("/chat")
async def chat(data: Chat):

    msg = data.message.lower()

    # detect reminder
    if "nhắc" in msg:

        time_match = re.search(r'\d{1,2}:\d{2}', msg)

        if time_match:

            time = time_match.group()

            today = datetime.now().date()
            time_str = f"{today}T{time}:00"

            create_reminder(msg, time_str)

            return {"reply": f"Đã lưu reminder lúc {time}"}


    # detect poster request
    if "poster" in msg or "ảnh" in msg:

        image_url = generate_poster(msg)

        return {
            "reply": "Đây là poster mình tạo:",
            "image": image_url
        }


    # normal AI chat
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant helping a Herbalife distributor create marketing content and manage reminders."
            },
            {"role": "user", "content": msg}
        ]
    )

    return {"reply": response.choices[0].message.content}


# ---------- WEB UI ----------

@app.get("/", response_class=HTMLResponse)
async def home():

    return """
    <html>
    <body>

    <h2>Mom AI Agent</h2>

    <input id="msg" style="width:300px" placeholder="Nhắn gì đó...">
    <button onclick="send()">Send</button>

    <div id="chat"></div>

    <script>

    async function send(){

        const msg=document.getElementById("msg").value

        const r=await fetch("/chat",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({message:msg})
        })

        const data=await r.json()

        document.getElementById("chat").innerHTML +=
        "<p><b>Mom:</b> "+msg+"</p>"

        if(data.image){
            document.getElementById("chat").innerHTML +=
            "<p><b>AI:</b> "+data.reply+"</p><img src='"+data.image+"' width=300>"
        }
        else{
            document.getElementById("chat").innerHTML +=
            "<p><b>AI:</b> "+data.reply+"</p>"
        }

    }

    </script>

    </body>
    </html>
    """
