# Create your views here.

from home.apps import channel
from proto import support_bot_pb2, support_bot_pb2_grpc

import grpc
import logging


def fetch_avatar_url(user_id):
    stub = support_bot_pb2_grpc.MetaHandlerStub(channel)
    request = support_bot_pb2.AvatarURLRequest(user_id=user_id)

    try:
        response = stub.FetchAvatarURL(request)
    except grpc.RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return None
    else:
        #if response.status_code:
        #    logging.error("Received error message: %s", response)
        return response.avatar_url