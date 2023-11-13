from django.contrib import admin
from core.models import Company, CostCenter


admin.site.register([Company, CostCenter])