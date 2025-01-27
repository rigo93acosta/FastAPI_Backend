from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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



@app.get("/usersjson")
async def usersjson():
    return [
        {"name": "Rigo", "surname": "Acosta", 
         "url": "https://rigo93acosta.github.io", "age": 27},
        {"name": "John", "surname": "Doe", 
         "url": "https://www.johndoe.com", "age": 30},
        {"name": "Jane", "surname": "Doe", 
         "url": "https://www.janedoe.com", "age": 25},
        {"name": "John", "surname": "Smith", 
         "url": "https://www.johnsmith.com", "age": 35},
        {"name": "Jane", "surname": "Smith", 
         "url": "https://www.janesmith.com", "age": 40},
    ]

@app.get("/users")
async def users():
    return users_list

# Path
@app.get("/username/{name}")
async def userByName(name: str):
    return searchUserByName(name)

# Query
@app.get("/username")
async def userByName(name: str):
    return searchUserByName(name)

# Path        
@app.get("/user/{user_id}")
async def userById(user_id: int):
    return searchUserById(user_id)

# Query
@app.get("/userquery/")
async def userQuery(user_id: int):
    return searchUserById(user_id)
    

@app.post("/user/")
async def createUser(user: User):
    if type(searchUserById(user.id)) == User:
        return {"message": "User already exists"}
    else:
        users_list.append(user)
    return user 

@app.delete("/delete/{user_id}")
async def deleteUser(user_id: int):
    user = searchUserById(user_id)
    if type(user) == User:
        users_list.remove(user)
        return {"message": "User deleted"}
    else:
        return {"message": "User not found"}
    
@app.put("/update/{user_id}")
async def updateUser(user_id: int, userNew: User):
    user = searchUserById(user_id)
    if type(user) == User:
        index = users_list.index(user)
        users_list.remove(user)
        users_list.insert(index, userNew)
        return {"message": "User updated"}
    else:
        return {"message": "User not found"}

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

