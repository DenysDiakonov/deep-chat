from auth.hash_utils import matchHashedText
import json
from auth.models import UserDBModel, UserManager
from core.exceptions import ValidationError
from core.decorators import with_response


@with_response
def register(event, context):
    try:
        new_user = UserDBModel(**json.loads(event["body"]))
    except:
        raise ValidationError()
    manager = UserManager()
    user = manager.create_user(new_user)
    return {"token": manager.get_token(user)}


@with_response
def login(event, context):
    try:
        new_user = UserDBModel(**json.loads(event["body"]))
    except:
        raise ValidationError()
    manager = UserManager()
    user = manager.get_user_by_username(new_user.username)
    if user != None and matchHashedText(user.password, new_user.password):
        return {"token": manager.get_token(user)}
    else:
        raise ValidationError("Email or password are incorrect")
