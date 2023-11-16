from django.contrib import admin
from core.models import Company, CostCenter, Department, Employee


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name', 'cnpj',)
    ordering = ('name',)


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    search_fields = ('company__name', 'code', 'description',)
    ordering = ('company__name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'cnpj')
    ordering = ('company__name', 'name', 'integration_code',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'email', 'city',)
    ordering = ('full_name',)
