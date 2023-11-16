import json

from model_bakery import baker, seq
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from core.models import CostCenter, Company, Department, Employee

def test_employee_viewset_list_(db):
    employee = baker.make(Employee, full_name=seq("user"), _quantity=2)

    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(f"/employees/")

    assert response.status_code == 200
    response = json.loads(response.content)
    assert len(response) == 2


def test_employee_viewset_create(db):
    employee = {
        "company": {
            "name": "Compeny",
            "cnpj": "21342121245322",
            "address": "Rua da praia 21",
            "city": "Rio de Jáneiro",
            "state": "RJ",
            "country": "Brasil"
        },
        "department": {
            "company": {
                "name": "Compeny",
                "cnpj": "21342121245322",
                "address": "Rua da praia 21",
                "city": "Rio de Jáneiro",
                "state": "RJ",
                "country": "Brasil"
            },
            "cost_center": {
                "company": {
                    "name": "Compeny",
                    "cnpj": "21342121245322",
                    "address": "Rua da praia 21",
                    "city": "Rio de Jáneiro",
                    "state": "RJ",
                    "country": "Brasil"
                },
                "code": "5",
                "description": "Cartão",
                "cost": "1111.00"
            },
            "name": "Construção",
            "integration_code": "25"
        },
        "full_name": "user",
        "email": "user@gmail.com",
        "phone_number": "(21)987654321",
        "birth_date": "2005-02-02",
        "entry_date": "2023-11-14",
        "departure_date": '2023-11-14',
        "city": "Rio de Janeiro"
    }

    user = baker.make(User)

    data = json.dumps(employee)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/employees/", data, content_type='application/json')

    assert response.status_code == 201
    
    employees = Employee.objects.all()
    
    assert len(employees)


def test_employee_viewset_update(db):
    baker.make(Employee, full_name="User2")
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    query_employee = Employee.objects.all().values()[0]

    assert query_employee['full_name'] == 'User2'

    updated_employee = {
        "full_name": "User"
    }

    response = client.put(f"/employees/{query_employee['id']}/", updated_employee)

    query_employee = Employee.objects.all().values()[0]

    assert query_employee['full_name'] == updated_employee['full_name']
    assert response.status_code == 200


def test_employee_viewset_destroy(db):
    baker.make(Employee)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
 
    query_employee = Employee.objects.all().values()[0]

    response = client.delete(f"/employees/{query_employee['id']}/")

    query_employee = Employee.objects.all()

    assert response.status_code == 204
    assert not len(query_employee)


def test_employee_viewset_list_not_authenticated(db):
    employee = baker.make(Employee, full_name="User")

    user = baker.make(User)

    client = APIClient()

    response = client.get("/employees/")

    assert response.status_code == 403


def test_employee_simple_list_ordered(db):
    employee1 = baker.make(Employee, full_name="Wuser")
    employee2 = baker.make(Employee, full_name="Yuser")
    employee3 = baker.make(Employee, full_name="Auser")
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/employees/?ordering=full_name")

    assert response.status_code == 200
    response = json.loads(response.content)
    
    assert employee3.full_name == response[0]['full_name'] # employee3.full_name = Auser 1º
    assert employee1.full_name == response[1]['full_name'] # employee1.full_name = Wuser 2º
    assert employee2.full_name == response[2]['full_name'] # employee2.full_name = Yuser 3º


def test_employee_simple_list_search(db):
    employee = baker.make(Employee, full_name="Wuser")
    baker.make(Employee, _quantity=6)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    all_active_employees = Employee.objects.all()

    assert len(all_active_employees) == 7

    response = client.get("/employees/?search=Wuser")

    assert response.status_code == 200
    response = json.loads(response.content)

    assert len(response) == 1
    assert response[0]['full_name'] == "Wuser"


def test_employee_simple_list_pagination(db):
    PAGE_SIZE = 10
    baker.make(Employee, _quantity=20)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/employees/?page=1")
    assert response.status_code == 200
    response = json.loads(response.content)

    assert len(response) == PAGE_SIZE
