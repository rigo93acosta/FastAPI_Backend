### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_scheme
from db.client import db_client


userDB = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

users_list = []


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
    

@userDB.post("/", response_model=User, 
             status_code=status.HTTP_201_CREATED)
async def createUser(user: User):
    # if type(searchUserById(user.id)) == User:
    #     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
    #                   detail="User already exists")
    # else:
    #     users_list.append(user)

    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_scheme(
        db_client.users.find_one({"_id": id})
        )

    return User(**new_user)

@userDB.delete("/{user_id}")
async def deleteUser(user_id: int):
    user = searchUserById(user_id)
    if type(user) == User:
        users_list.remove(user)
        return {"message": "User deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
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
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
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

