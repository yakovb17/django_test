from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_url),
    path('s/<str:key>', views.redirect_url),
    path('key_data/<str:key>', views.get_key_data),
]
