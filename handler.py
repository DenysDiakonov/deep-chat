from core.utils import get_response
from core.decorators import with_response
import logging

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)


@with_response
def ping(event, context):
    logger.info("Ping requested.")
    return "Pong!"


def connection_manager(event, context):
    print(event)
    print(context)

    if event["requestContext"]["eventType"] == "CONNECT":
        print("Connect successful.")
        return get_response(200, "Connect successful.")

    elif event["requestContext"]["eventType"] == "DISCONNECT":
        print("Disconnect successful.")
        return get_response(200, "Disconnect successful.")

    else:
        logger.error(
            "Connection manager received unrecognized eventType '{}'".format(
                event["requestContext"]["eventType"]
            )
        )
        return get_response(500, "Unrecognized eventType.")
