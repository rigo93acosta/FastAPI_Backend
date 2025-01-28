### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_scheme, users_scheme_list
from db.client import db_client
from bson import ObjectId

userDB = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})


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

@userDB.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(user_id: str):

    found = db_client.users.find_one_and_delete(
        {"_id": ObjectId(user_id)}
        )
    
    if not found:
        return {"message": "User not found"} 


@userDB.put("/", response_model=User)
async def updateUser(userNew: User):
    ...
    

def searchUser(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_scheme(user))
    except:
        return {"message": "User not found"}