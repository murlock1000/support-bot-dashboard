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

#def fetch_room_messages(room_id:str) -> Union[dict, RpcError]:
#    stub = support_bot_pb2_grpc.RoomHandlerStub(channel)
#    request = support_bot_pb2.AvatarURLRequest(user_id=user_id)
#    try:
#        response = stub.FetchAvatarURL(request)
#        return response.avatar_url
#    except RpcError as rpc_error:
#        logging.error("Received error: %s", rpc_error)
#        return rpc_error

def unassign_staff_from_ticket(user_id:str, ticket_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.UserWithTicketRequest(user_id=user_id, ticket_id=ticket_id)
    try:
        stub.RemoveStaffFromTicket(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error
    
def unassign_staff_from_chat(user_id:str, chat_room_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.UserWithChatRequest(user_id=user_id, chat_room_id=chat_room_id)
    try:
        stub.RemoveStaffFromChat(request)
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
    
def close_chat(chat_room_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.ChatRequest(chat_room_id=chat_room_id)
    try:
        stub.CloseChat(request)
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
    
def delete_ticket_room(ticket_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.TicketRequest(ticket_id=ticket_id)
    try:
        stub.DeleteTicketRoom(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error
    
def delete_chat_room(chat_room_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.ChatRequest(chat_room_id=chat_room_id)
    try:
        stub.DeleteChatRoom(request)
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
    
def claim_chat_for_staff(user_id:str, chat_room_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.UserWithChatRequest(user_id=user_id, chat_room_id=chat_room_id)
    try:
        stub.ClaimChat(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error
    
def claim_chat_for_support(user_id:str, chat_room_id:str) -> Optional[RpcError]:
    stub = support_bot_pb2_grpc.CommandHandlerStub(channel)
    request = support_bot_pb2.UserWithChatRequest(user_id=user_id, chat_room_id=chat_room_id)
    try:
        stub.ClaimForChat(request)
    except RpcError as rpc_error:
        logging.error("Received error: %s", rpc_error)
        return rpc_error