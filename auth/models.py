import os
import jwt
from pydantic import BaseModel

from core.db import dynamodb
from core.exceptions import ValidationError

from auth.hash_utils import hashText


class UserDBModel(BaseModel):
    username: str
    password: str


class UserManager:
    def __init__(self) -> None:
        self.table = dynamodb.Table("User")

    def get_token(self, user: UserDBModel) -> str:
        return jwt.encode(
            {"username": "denthegreat"},
            os.getenv("JWT_SECRET"),
            algorithm="HS256",
        )

    def get_user_by_username(self, username: str) -> UserDBModel:
        table = dynamodb.Table("User")
        user_data = table.get_item(Key={"username": username}).get("Item")
        if user_data != None:
            return UserDBModel(**user_data)
        else:
            return None

    def get_user_by_token(self, token: str) -> UserDBModel:
        try:
            token_data = jwt.decode(
                token, os.getenv("JWT_SECRET"), algorithms=["HS256"]
            )
            username = token_data["username"]
        except:
            raise ValidationError("Invalid token")
        user = self.get_user_by_username(username)
        if user != None:
            return user
        else:
            raise ValidationError("User not found", 404)

    def create_user(self, new_user: UserDBModel) -> UserDBModel:
        check = self.get_user_by_username(new_user.username)
        if check == None:
            user = UserDBModel(
                username=new_user.username, password=hashText(new_user.password)
            )
            self.table.put_item(Item=user.dict())
            return user
        else:
            raise ValidationError("Such user already exists")
