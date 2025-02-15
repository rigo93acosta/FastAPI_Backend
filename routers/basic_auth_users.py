from fastapi import FastAPI, Depends, HTTPException, status
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
        "full_name" : "Rigoberto Acosta",
        "email" : "rigo93acosta@gmail.com",
        "disable" : False,
        "password" : "654321"
    },
    "riacosta2": {
        "username" : "riacosta2",
        "full_name" : "Rigoberto Acosta ",
        "email" : "rigo93acosta2@gmail.com",
        "disable" : True,
        "password" : "123456"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])

def search_user(username: str):  
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid credentials", 
        headers={"WWW-Authenticate": "Bearer"})
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Inactive user")
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    
    user = search_user_db(form.username)
    if not user.password == form.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(user: User = Depends(current_user)):
    return user
