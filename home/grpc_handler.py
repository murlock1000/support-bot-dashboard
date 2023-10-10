# Create your views here.

from typing import Optional, Union
from home.apps import channel
from proto import support_bot_pb2, support_bot_pb2_grpc

from grpc import (
    RpcError
)
import logging


def fetch_avatar_url(user_id:str) -> Union[str, RpcError]:
    stub = support_bot_pb2_grpc.MetaHandlerStub(channel)
    request = support_bot_pb2.AvatarURLRequest(user_id=user_id)
    try:
        response = stub.FetchAvatarURL(request)
        return response.avatar_url
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error
        
def unassign_staff_from_ticket(user_id:str, ticket_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.UserWithTicketRequest(user_id=user_id, ticket_id=ticket_id)
    try:
        stub.RemoveStaffFromTicket(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error
    
def close_ticket(ticket_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.TicketRequest(ticket_id=ticket_id)
    try:
        stub.CloseTicket(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error
    
def reopen_ticket(ticket_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.TicketRequest(ticket_id=ticket_id)
    try:
        stub.ReopenTicket(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error
    
def claim_ticket_for_staff(user_id:str, ticket_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.UserWithTicketRequest(user_id=user_id, ticket_id=ticket_id)
    try:
        stub.ClaimTicket(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error
    
def claim_ticket_for_support(user_id:str, ticket_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.UserWithTicketRequest(user_id=user_id, ticket_id=ticket_id)
    try:
        stub.ClaimForTicket(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error