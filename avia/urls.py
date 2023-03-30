from django.urls import path
from . import views

urlpatterns = [
    path("", views.search_aircraft, name="search_aircraft"),
]
