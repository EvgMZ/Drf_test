from django.urls import path
from . import views
urlpatterns = [
    path('list', views.list_view, name='list_page'),
    path('', views.home_page, name='home_page')
]
