### Users DB API ###

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

userDB = APIRouter(prefix="/userdb",
                        tags=["usersdb"],
                         responses={404: {"description": "Not found"}})

# Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [
        User(id=1, name="Rigo", surname="Acosta",
                    url="https://rigo93acosta.github.io", age=27),
        User(id=2, name="John", surname="Doe",
                    url="https://www.johndoe.com", age=30),
        User(id=3, name="Jane", surname="Doe",
                    url="https://www.janedoe.com", age=25),
        User(id=4, name="John", surname="Smith",
                    url="https://www.johnsmith.com", age=35),
        User(id=5, name="Jane", surname="Smith",
                    url="https://www.janesmith.com", age=40)
        ]


@userDB.get("/")
async def users():
    return users_list

# Path        
@userDB.get("/{user_id}")
async def userById(user_id: int):
    return searchUserById(user_id)

# Query
@userDB.get("/")
async def userQuery(user_id: int):
    return searchUserById(user_id)
    

@userDB.post("/", response_model=User, status_code=201)
async def createUser(user: User):
    if type(searchUserById(user.id)) == User:
        raise HTTPException(status_code=204, 
                      detail="User already exists")
    else:
        users_list.append(user)
    return user 

@userDB.delete("/{user_id}")
async def deleteUser(user_id: int):
    user = searchUserById(user_id)
    if type(user) == User:
        users_list.remove(user)
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=204, 
                      detail="User not found")
    
@userDB.put("/")
async def updateUser(userNew: User):
    user = searchUserById(userNew.id)
    if type(user) == User:
        index = users_list.index(user)
        users_list.remove(user)
        users_list.insert(index, userNew)
        return {"message": "User updated"}
    else:
        raise HTTPException(status_code=204, 
                      detail="User not found")

## Functions
def searchUserById(user_id: int):
    user = filter(lambda user: user.id == user_id, users_list)
    try:
        return list(user)[0]
    except:
        return {"message": "User not found"}

def searchUserByName(name: str):
    user = filter(lambda user: user.name == name, users_list)
    try:
        return list(user)[0]
    except:
        return {"message": "User not found"}

