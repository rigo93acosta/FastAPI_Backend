from fastapi import FastAPI
from routers import users, products

app = FastAPI()

## Routers

app.include_router(users.user_router)
app.include_router(products.router_product)

@app.get("/")
async def root():
    return {"message": "Hello World motherfuckers!"}

@app.get("/url")
async def url():
    return {"url": "https://rigo93acosta.github.io"}