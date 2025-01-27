from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Entidad User
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

# Entidad UserInDB
class UserInDB(User):
    password: str
# Database
users_db = {
    "riacosta": {
        "username" : "riacosta",
        "fullname" : "Rigoberto Acosta",
        "email" : "rigo93acosta@gmail.com",
        "disable" : False,
        "password" : "654321"
    },
    "riacosta2": {
        "username" : "riacosta2",
        "fullname" : "Rigoberto Acosta ",
        "email" : "rigo93acosta2@gmail.com",
        "disable" : True,
        "password" : "123456"
    }
}



def search_user(username: str):
    
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(user_dict)
    return None


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    user = search_user(form.username)

    if not user_db.password == form.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    else:
        ...
    
    