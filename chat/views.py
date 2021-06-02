from chat.ws_utils import send_to_connection
from chat.models import ChatConnectionManager, MessageCreateModel, MessageManager
from core.exceptions import APIException, ValidationError
from core.decorators import with_response
from core.utils import get_body

from auth.models import UserManager


@with_response
def connection_manager(event, context):
    connection_id = event["requestContext"].get("connectionId")
    token = event.get("queryStringParameters", {}).get("token")
    room = event.get("queryStringParameters", {}).get("room")

    if event["requestContext"]["eventType"] == "CONNECT":
        if not connection_id:
            raise APIException("connectionId value not set.")
        if not token:
            raise ValidationError("token query parameter not provided.")
        if not room:
            raise ValidationError("room query parameter not provided.")

        UserManager().get_user_by_token(token)
        ChatConnectionManager().create(connection_id, room)

        return "Connect successful."

    elif event["requestContext"]["eventType"] == "DISCONNECT":
        if not connection_id:
            raise APIException("connectionId value not set.")

        ChatConnectionManager().delete(connection_id)

        return "Disconnect successful."

    else:
        raise APIException("Unrecognized eventType")


@with_response
def default_message(event, context):
    raise ValidationError("Unrecognized WebSocket action.")


@with_response
def send_message(event, context):
    id = event["requestContext"].get("connectionId")
    if not id:
        raise APIException("connectionId value not set.")

    body = get_body(event)

    if not isinstance(body, dict):
        raise ValidationError("Message body not in dict format.")
    for attribute in ["token", "content"]:
        if attribute not in body:
            raise ValidationError(f"'{attribute}' not in message dict")

    token = body["token"]
    user = UserManager().get_user_by_token(token)
    username = user.username

    content = body["content"]

    conn_manager = ChatConnectionManager()
    room = conn_manager.get_room_by_connection(id)

    item = MessageCreateModel(room=room, username=username, content=content)
    message = MessageManager().create(item)
    connections = conn_manager.get_connections_by_room(room)

    message = {
        "username": message.username,
        "content": message.content,
        "timestamp": message.timestamp,
    }
    data = {"messages": [message]}
    for id in connections:
        try:
            send_to_connection(id, data, event)
        except:
            conn_manager.delete(id)
    return f"Message sent to {len(connections)} connections."


@with_response
def get_recent_messages(event, context):
    id = event["requestContext"].get("connectionId")
    if not id:
        raise APIException("connectionId value not set.")

    room = ChatConnectionManager().get_room_by_connection(id)
    msgs = MessageManager().get_history(room)

    data = {"messages": msgs}
    send_to_connection(id, data, event)

    return f"Sent recent messages to '{id}'."
