from django.contrib import admin
from core.models import Company, CostCenter, Department, Employee


admin.site.register([Company, CostCenter, Department, Employee])