from time import time
from urllib.parse import urlparse
from django.conf import settings
from django_telemetry.models import WebTelemetry,WebQuery
from django.contrib.auth.models import User
import json
import sys
from django.db import connection

from django.http import HttpResponsePermanentRedirect, JsonResponse

def dumps(value):
    return json.dumps(value,default=lambda o:None)


class WebTelemetryMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        start_time = time()
        try:
            path_array = request.path.split('/')
            if 'admin' == path_array[1]:
                pass
            elif 'telemetry' == path_array[1]:
                pass
            else:  
                self.save(request, response,int((time()-start_time)*1000*1000))
        except Exception as e:
            print(sys.stderr, "Error saving request log", e)

        return response



    def save(self, request, response,duration_time):
        if hasattr(request, 'user'):
            user_id = request.user.id if type(request.user) == User else None
        else:
            user_id = None

        meta = request.META.copy()
        meta.pop('QUERY_STRING',None)
        meta.pop('HTTP_COOKIE',None)
        remote_addr_fwd = None

        if 'HTTP_X_FORWARDED_FOR' in meta:
            remote_addr_fwd = meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
            if remote_addr_fwd == meta['HTTP_X_FORWARDED_FOR']:
                meta.pop('HTTP_X_FORWARDED_FOR')

        post = None

        try:
            post = request.POST
        except Exception as e:
            post = request.body
        
    

        tel = WebTelemetry.objects.using('django_telemetry').create(
            host = request.get_host(),
            path = request.path,
            headers = request.headers,
            method = request.method,
            uri = request.build_absolute_uri(),
            status_code = response.status_code,
            user_agent = meta.pop('HTTP_USER_AGENT',None),
            remote_addr = meta.pop('REMOTE_ADDR',None),
            remote_addr_fwd = remote_addr_fwd,
            meta = None if not meta else dumps(meta),
            cookies = None if not request.COOKIES else dumps(request.COOKIES),
            get = None if not request.GET else dumps(request.GET),
            post =post,
            raw_post = request.body,
            is_secure = request.is_secure(),
            response=response.content,
            is_ajax = True,
            user_id = user_id,
            duration=duration_time,
        )

        for query in connection.queries:
            WebQuery.objects.using('django_telemetry').create(sql=query['sql'],time=query['time'],telemetry=tel)
        
       
