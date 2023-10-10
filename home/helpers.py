from enum import Enum

from django.http import HttpRequest


class ReqType(Enum):
    GET = "GET",
    POST = "POST"

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def validateAjaxRequest(request:HttpRequest, reqType: ReqType):
    if request.method != reqType.value:
        raise ValueError(f"Request type not {reqType.value}")
    
    if not is_ajax(request):
        raise ValueError("Ajax not set")

    if not request.user:
        raise ValueError("User not found")