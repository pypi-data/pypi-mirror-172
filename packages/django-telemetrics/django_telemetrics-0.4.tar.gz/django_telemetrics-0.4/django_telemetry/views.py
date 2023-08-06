from pprint import pprint
from django.shortcuts import render
from django_telemetry.models import WebTelemetry,WebQuery
from django.core.paginator import Paginator
import json
from ast import literal_eval

def main_view(request):

    telemetries = WebTelemetry.objects.all().order_by('-time')

    method_type = request.GET.get('method_type',None)
    status_code = request.GET.get('status_code',None)
    search = request.GET.get('search',None)

    if search != None:
        telemetries = telemetries.filter(path__icontains=search)

    if method_type != None and method_type != 'Все':
        telemetries = telemetries.filter(method=method_type)
    
    if status_code != None and status_code != 'Все':
        telemetries = telemetries.filter(status_code=status_code)

    count_of_telemetries = telemetries.count()
    count_of_queries = WebQuery.objects.all().count()
    
    paginator = Paginator(telemetries, 25)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)

    data = {
        'count_of_telemetries': count_of_telemetries,
        'count_of_queries': count_of_queries,
        'telemetries': page_obj
    }
    return render(request,'telemetry/main.html',context=data)


def detail_request_view(request,uuid):

    telemetry = WebTelemetry.objects.get(uuid=uuid)

    meta = json.loads(telemetry.meta)
    meta_data = json.dumps(meta, indent=4)

    try:
        get = json.loads(telemetry.get)
        get_data = json.dumps(get, indent=4)
    except Exception as e:
        get_data = telemetry.get
    

    try:
        post = json.loads(telemetry.post)
        post_data = json.dumps(post, indent=4)
    except Exception as e:
        post_data = telemetry.get

    data = {
        'telemetry': telemetry,
        'meta': meta_data,
        'get':get_data,
        'post': post_data
    }

    return render(request,'telemetry/detail_request.html',context=data)
