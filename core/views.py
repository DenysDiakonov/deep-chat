from core.decorators import with_response


@with_response
def ping(event, context):
    return "Pong!"
