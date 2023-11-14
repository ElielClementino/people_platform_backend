import pytest
from model_bakery import baker

from core.models import Company, Employee, Department


def test_if_soft_delete_is_working(db):
    company = baker.make(Company)

    companies = Company.objects.all()
    
    assert len(companies) == 1
    assert companies[0].is_active

    company.delete()
    company.refresh_from_db()

    companies = Company.all_objects.all()
    
    assert len(companies) == 1
    assert not companies[0].is_active


def test_if_soft_delete_cascade_is_deleting_only_the_right_object(db):
    company = baker.make(Company)
    company2 = baker.make(Company)

    employee = baker.make(Employee, company=company)
    employee2 = baker.make(Employee, company=company2)

    company.delete()
    employee.refresh_from_db()
    employee2.refresh_from_db()

    assert not employee.is_active
    assert employee2.is_active


def test_if_soft_delete_cascade_is_deleting_only_forward_not_backward(db):
    company = baker.make(Company)

    department = baker.make(Department, company=company)

    employee = baker.make(Employee, company=company, department=department)

    department.delete()
    company.refresh_from_db()
    employee.refresh_from_db()

    assert not department.is_active
    assert not employee.is_active
    assert company.is_active


def test_if_manager_is_retriving_only_where_is_active(db):
    company = baker.make(Company)
    company2 = baker.make(Company)

    companies = Company.objects.all()

    assert len(companies) == 2

    company.delete()
    company.refresh_from_db()
    company2.refresh_from_db

    companies = Company.objects.all()

    assert len(companies) == 1


def test_if_manager_is_retriving_where_not_active(db):
    company = baker.make(Company)
    company.delete()
    company.refresh_from_db()

    companies = Company.objects.all()

    assert len(companies) == 0

    companies = Company.all_objects.all()

    assert len(companies) == 1
    assert not companies[0].is_active
