from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from time import strftime
import os


def whoami(request) -> HttpResponse:
    """
    Provides information about the client
    :param request: contains metadata about the request
    :return: views as an instance of a class HttpResponse
    """
    undefined: str = 'undefined'
    data: dict = {
        'user_agent': request.META.get('HTTP_USER_AGENT', undefined),
        'ip_client': request.META.get('REMOTE_ADDR', undefined),
        'time': strftime('%H:%M:%S')
    }
    return HttpResponse(f'<div><p><b>Browser:</b> {data["user_agent"]}</p>'
                        f'<p><b>IP address:</b> {data["ip_client"]}</p>'
                        f'<p><b>Time Server:</b> {data["time"]}</p></div>')


def source_code(request) -> HttpResponse:
    """
    Shows the source code of the current file
    :param request: contains metadata about the request
    :return: views as an instance of a class HttpResponse
    """
    script_file_name: str = __file__.split('/')[-1]
    target_path: str = f'{settings.BASE_DIR}/{__name__.split(".")[0]}'
    os.chdir(target_path)
    with open(script_file_name, 'r') as f:
        yourself_data = f.read()
        yourself_data = yourself_data.replace('<', '&lt;').replace('>', '&gt')
    return HttpResponse(f'<pre>{yourself_data}</pre>')
