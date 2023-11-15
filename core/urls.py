from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views
from core import viewsets

router = DefaultRouter()
router.register(r"companies", viewsets.CompanyViewSet, basename="company")


urlpatterns = [
    path("throwexce", views.throw_exce),
    path("", include(router.urls)),
]
