from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("extract_math/", views.extract_math, name="extract_math"),
]
