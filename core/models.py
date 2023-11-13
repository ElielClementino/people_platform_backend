from django.db import models
from .common.managers import BaseModel, BaseModelManager

class Company(BaseModel):
    name = models.TextField()
    cnpj = models.CharField(max_length=14, unique=True, null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CostCenter(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="cost_centers")
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateField(auto_now_add=True)
