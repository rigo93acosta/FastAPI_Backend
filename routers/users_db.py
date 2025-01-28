### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_scheme, users_scheme_list
from db.client import db_client
from bson import ObjectId

userDB = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

users_list = []


@userDB.get("/", response_model=list[User])
async def users():
    return users_scheme_list(db_client.users.find())

# Path        
@userDB.get("/{user_id}")
async def userById(user_id: str):
    return searchUser("_id", ObjectId(user_id))

# Query
@userDB.get("/")
async def userQuery(user_id: str):
    return searchUser("_id", ObjectId(user_id))
    

@userDB.post("/", response_model=User, 
             status_code=status.HTTP_201_CREATED)
async def createUser(user: User):
    if type(searchUser("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                      detail="User already exists")

    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_scheme(
        db_client.users.find_one({"_id": id})
        )

    return User(**new_user)

@userDB.delete("/{user_id}")
async def deleteUser(user_id: int):
    user = searchUserByName(user_id)
    if type(user) == User:
        users_list.remove(user)
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                      detail="User not found")
    
@userDB.put("/")
async def updateUser(userNew: User):
    user = searchUserByName(userNew.id)
    if type(user) == User:
        index = users_list.index(user)
        users_list.remove(user)
        users_list.insert(index, userNew)
        return {"message": "User updated"}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                      detail="User not found")

## Functions
def searchUserById(user_id: int):
    ...

def searchUserByName(name: str):
    ...
    
def searchUser(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_scheme(user))
    except:
        return {"message": "User not found"}