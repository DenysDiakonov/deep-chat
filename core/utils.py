import os
import json

from core.exceptions import APIException


def get_response(status_code, body):
    if not isinstance(body, str):
        try:
            body = json.dumps(body)
        except:
            raise APIException("Given body is not JSON-serializible")
    origin = os.getenv("CORS_ORIGIN", "*")

    return {
        "statusCode": status_code,
        "body": body,
        "headers": {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": True,
        },
    }


def get_body(event):
    try:
        return json.loads(event.get("body", ""))
    except:
        raise APIException("Event body could not be JSON decoded.")
