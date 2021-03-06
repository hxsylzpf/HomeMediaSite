# noinspection PyBroadException
import json
import traceback
from django.http import HttpResponse


# noinspection PyBroadException
def get_request_with_default(request, key, default_value):
    """
    Try to get value by specific key in request object, if can't find key in keySet, return default value.
    :param request: request object created by django
    :param key: key
    :param default_value: default value
    :return: 
    """
    try:
        return request.GET[key]
    except:
        return default_value


def get_request_get(request, key):
    """
    Try to get value by specific key in request object, if can't find key in keySet, return None.
    :param request: request object created by django
    :param key: key
    :return: 
    """
    return get_request_with_default(request, key, None)


def get_json_response(obj):
    """
    Create a http response 
    :param obj: object which json serializable 
    :return: 
    """
    return HttpResponse(json.dumps(obj))


def get_host(request):
    """
    Get host info from request META
    :param request: 
    :return: 
    """
    return request.META["HTTP_HOST"].split(":")[0]


def response_json_error_info(func):
    """
    Trying to run function, if exception caught, return error details with json format
    :param func: 
    :return: 
    """
    def wrapper(request):
        try:
            return func(request)
        except Exception as ex:
            return get_json_response({
                "status": "error",
                "error_info": str(ex),
                "trace_back": traceback.format_exc()
            })

    return wrapper


def response_json(func):
    """
    Trying to run function, if exception caught, return error details with json format, else return json formatted object
    :param func: 
    :return: 
    """
    def wrapper(request):
        try:
            return get_json_response(func(request))
        except Exception as ex:
            return get_json_response({
                "status": "error",
                "error_info": str(ex),
                "trace_back": traceback.format_exc()
            })

    return wrapper
