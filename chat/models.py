import time

from pydantic import BaseModel

from core.db import dynamodb
from core.exceptions import APIException


class ChatConnectionDBModel(BaseModel):
    connection_id: str
    room: str


class ChatConnectionManager:
    def __init__(self) -> None:
        self.table = dynamodb.Table("deep_chat_connection")

    def create(self, id: str, room: str) -> ChatConnectionDBModel:
        conn = ChatConnectionDBModel(connection_id=id, room=room)
        self.table.put_item(Item=conn.dict())
        return conn

    def delete(self, id: str) -> None:
        self.table.delete_item(Key={"connection_id": id})

    def get_connections_by_room(self, room):
        response = self.table.scan(
            FilterExpression="room = :room",
            ExpressionAttributeValues={":room": room},
        )
        items = response.get("Items", [])
        return [x["connection_id"] for x in items if "connection_id" in x]

    def get_room_by_connection(self, id):
        response = self.table.query(
            KeyConditionExpression="connection_id = :connection_id",
            ExpressionAttributeValues={":connection_id": id},
            Limit=1,
        )
        items = response.get("Items")
        if len(items) != 1:
            raise APIException("Invalid room by connection")
        room_item = items[0]
        return room_item["room"]

    def get_other_connections(self, id):
        room = self.get_room_by_connection(id)
        return self.get_connections_by_room(room)


class MessageCreateModel(BaseModel):
    room: str
    username: str
    content: str


class MessageDBModel(MessageCreateModel):
    index: int
    timestamp: int


class MessageManager:
    def __init__(self) -> None:
        self.table = dynamodb.Table("deep_chat_messages")

    def get_new_index(self, room: str) -> int:
        response = self.table.query(
            KeyConditionExpression="room = :room",
            ExpressionAttributeValues={":room": room},
            Limit=1,
            ScanIndexForward=False,
        )
        items = response.get("Items", [])
        return items[0]["index"] + 1 if len(items) > 0 else 0

    def create(self, item: MessageCreateModel) -> MessageDBModel:
        new_item = MessageDBModel(
            **(item.dict()),
            index=self.get_new_index(item.room),
            timestamp=int(time.time())
        )
        self.table.put_item(Item=new_item.dict())
        return new_item

    def get_history(self, room):
        response = self.table.query(
            KeyConditionExpression="room = :room",
            ExpressionAttributeValues={":room": room},
            Limit=100,
            ScanIndexForward=True,
        )
        items = response.get("Items", [])

        messages = [
            {
                "username": i["username"],
                "content": i["content"],
                "timestamp": int(i["timestamp"]),
            }
            for i in items
        ]
        messages.reverse()

        return messages
