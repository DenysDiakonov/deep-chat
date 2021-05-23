import json
import boto3


def send_to_connection(connection_id, data, event):
    gatewayapi = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url="https://"
        + event["requestContext"]["domainName"]
        + "/"
        + event["requestContext"]["stage"],
    )
    return gatewayapi.post_to_connection(
        ConnectionId=connection_id, Data=json.dumps(data).encode("utf-8")
    )
