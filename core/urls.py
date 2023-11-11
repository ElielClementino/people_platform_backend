from django.urls import path

from . import views

urlpatterns = [
    path("throwexce", views.throw_exce),
]