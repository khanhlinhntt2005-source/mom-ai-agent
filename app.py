from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "write a short facebook post about healthy lifestyle"}
    ]
)

print(response.choices[0].message.content)

from fastapi.responses import FileResponse
from fastapi import FastAPI

app = FastAPI()

@app.get("/zalo_verifierHjI6Byt507COiArMvAKUJpoWZrRGrbi0DZan.html")
def verify():
    return FileResponse("zalo_verifierHjI6Byt507COiArMvAKUJpoWZrRGrbi0DZan.html")
