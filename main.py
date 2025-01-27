from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World motherfuckers!"}

@app.get("/url")
async def url():
    return {"url": "https://rigo93acosta.github.io"}