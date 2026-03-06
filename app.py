from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/zalo_verifierHjI6Byt507COiArMvAKUJpoWZrRGrbi0DZan.html")
def verify():
    return FileResponse("zalo_verifierHjI6Byt507COiArMvAKUJpoWZrRGrbi0DZan.html")
