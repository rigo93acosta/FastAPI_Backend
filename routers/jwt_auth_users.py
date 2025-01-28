from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import jwt
from jwt.exceptions import InvalidTokenError, PyJWTError
from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = "HS256" # HMAC with SHA-256
ACCESS_TOKEN_DURATION = 1 # 1 minute
SECRET_KEY = "701a7e691a04870b027d720548e55db32afc12d9fd420fe6f7e9694fbff3a0bb"
crypt = CryptContext(schemes=["bcrypt"]) # bcrypt


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
        "password" : "$2a$12$g74VQu1mxXfROyiKCe8zFOAuY1M/Iaviewsg6ia0asGPPzmW7jXtS"
    },
    "riacosta2": {
        "username" : "riacosta2",
        "full_name" : "Rigoberto Acosta ",
        "email" : "rigo93acosta2@gmail.com",
        "disable" : True,
        "password" : "$2a$12$b3mothKL0o1iX69R/85iVuNMEzyn/GVskzrUm5BayrHlLj2w7Nkje"
    }
}

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, 
                            detail="Incorrect username")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, 
                            detail="Incorrect password")
    
    access_token = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc) \
            + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    return {"access_token": jwt.encode(access_token, 
                                       key=SECRET_KEY,
                                       algorithm=ALGORITHM), 
            "token_type": "bearer"}

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials", 
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except PyJWTError:
        raise exception
    
    return search_user(username)
    

async def current_user(user_token: User = Depends(auth_user)):
    if user_token.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Inactive user")
    return user_token

@app.get("/users/me")
async def read_users_me(user: User = Depends(current_user)):
    return user

def search_user_db(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])

def search_user(username: str):  
    if username in users_db:
        return User(**users_db[username])