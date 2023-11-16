from django.db import models
from .common.managers import BaseModel


class Company(BaseModel):
    name = models.TextField()
    cnpj = models.CharField(max_length=14, unique=True, null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}--{self.cnpj}--{self.state}"


class CostCenter(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="cost_centers")
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}-{self.description}-{self.company.name}"


class Department(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="departments")
    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=100)
    integration_code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    full_name = models.CharField(max_length=125)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=25)
    birth_date = models.DateField()
    entry_date = models.DateField()
    departure_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} - {self.company.name} - {self.department}"
