from chat.models import ChatConnectionManager
from core.exceptions import APIException, ValidationError
from core.decorators import with_response

from auth.models import UserManager


@with_response
def connection_manager(event, context):
    print(event)
    connection_id = event["requestContext"].get("connectionId")
    token = event.get("queryStringParameters", {}).get("token")

    print(connection_id)
    print(token)

    if event["requestContext"]["eventType"] == "CONNECT":
        if not connection_id:
            print("Failed: connectionId value not set.")
            raise APIException("connectionId value not set.")
        if not token:
            print("Failed: token query parameter not provided.")
            raise ValidationError("token query parameter not provided.")

        UserManager().get_user_by_token(token)
        ChatConnectionManager().create(connection_id)

        print("Connect successful.")
        return "Connect successful."

    elif event["requestContext"]["eventType"] == "DISCONNECT":
        if not connection_id:
            print("Failed: connectionId value not set.")
            raise APIException("connectionId value not set.")

        ChatConnectionManager().delete(connection_id)

        print("Disconnect successful.")
        return "Disconnect successful."

    else:
        print(
            "Connection manager received unrecognized eventType '{}'".format(
                event["requestContext"]["eventType"]
            )
        )
        raise APIException("Unrecognized eventType")
