from pydantic import BaseModel

from core.db import dynamodb
from core.exceptions import ValidationError


class ChatConnectionDBModel(BaseModel):
    connection_id: str


class ChatConnectionManager:
    def __init__(self) -> None:
        self.table = dynamodb.Table("deep_chat_connection")

    def create(self, id: str) -> ChatConnectionDBModel:
        conn = ChatConnectionDBModel(connection_id=id)
        self.table.put_item(Item=conn.dict())
        return conn

    def delete(self, id: str) -> None:
        conn = ChatConnectionDBModel(connection_id=id)
        self.table.delete_item(Key=conn.dict())
