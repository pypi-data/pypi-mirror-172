from django.urls import path
from .views import main_view,detail_request_view

urlpatterns = [
    path('',main_view,name='main_view'),
    path('requests/<str:uuid>/',detail_request_view,name='detail_request_view')
]