from fastapi import FastAPI
from routers import users, products
from fastapi.staticfiles import StaticFiles

app = FastAPI()

## Routers

app.include_router(users.user_router)
app.include_router(products.router_product)
app.mount("/static", 
           StaticFiles(directory="static"), 
           name="static")

@app.get("/")
async def root():
    return {"message": "Hello World motherfuckers!"}

@app.get("/url")
async def url():
    return {"url": "https://rigo93acosta.github.io"}