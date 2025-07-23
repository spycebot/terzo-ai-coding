from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/assist")
async def assist(request: Request):
    data = await request.json()
    # Process with your assistant
    return {"response": "..."}