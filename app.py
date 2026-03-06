from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/zalo_verifierHjI6Byt507COiArMvAKUJpoWZrRGrbi0DZan.html")
def verify():
    return FileResponse("zalo_verifierHjI6Byt507COiArMvAKUJpoWZrRGrbi0DZan.html")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(data)
    return {"status": "ok"}
