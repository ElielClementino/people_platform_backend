from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter

from core.models import Company, CostCenter, Department, Employee
from core.serializers.company_serializer import CompanySerializer
from core.serializers.cost_center_serializer import CostCenterSerializer
from core.serializers.department_serializer import DepartmentSerializer
from core.serializers.employee_serializer import EmployeeSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ('name', 'cnpj')

    def list(self, request):
        companies = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(companies)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(companies, many=True)

        if page is not None:
            return Response(serializer.data)

        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CostCenterViewSet(viewsets.ModelViewSet):
    queryset = CostCenter.objects.all()
    serializer_class = CostCenterSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ('company__name', 'code', 'description')

    def list(self, request):
        cost_centers = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(cost_centers)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(cost_centers, many=True)

        if page is not None:
            return Response(serializer.data)

        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
