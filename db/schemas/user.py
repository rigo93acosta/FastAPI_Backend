def user_scheme(user) -> dict:

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }
