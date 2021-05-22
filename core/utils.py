from core.exceptions import APIException
import json


def get_response(status_code, body):
    if not isinstance(body, str):
        try:
            body = json.dumps(body)
        except:
            raise APIException("Given body is not JSON-serializible")
    return {"statusCode": status_code, "body": body}
