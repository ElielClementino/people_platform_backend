from django.contrib import admin
from core.models import Company, CostCenter, Department, Employee


admin.site.register([CostCenter, Department, Employee])

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj')
    search_fields = ('name', 'cnpj')
    list_filter = ('name',)
    ordering = ('name',)
