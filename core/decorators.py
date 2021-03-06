from core.exceptions import APIException, ValidationError
from core.utils import get_response


def with_response(func):
    def wrapper(event, context):
        code = 200
        try:
            response = func(event, context)
        except ValidationError as e:
            response = {"detail": e.detail}
            code = e.code
        except APIException as e:
            response = {"detail": e.detail}
            code = e.code
        if isinstance(response, tuple):
            response, code = response
        print(response)
        return get_response(code, response)

    return wrapper
