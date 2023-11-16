from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views
from core import viewsets

router = DefaultRouter()
router.register(r"companies", viewsets.CompanyViewSet, basename="company")
router.register(r"cost_centers", viewsets.CostCenterViewSet, basename="cost_center")


urlpatterns = [
    path("throwexce", views.throw_exce),
    path("", include(router.urls)),
]
