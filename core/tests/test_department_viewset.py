import json

from model_bakery import baker, seq
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from core.models import CostCenter, Company, Department

def test_department_viewset_list_(db):
    department = baker.make(Department, name="Tecnologia", _quantity=2)

    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(f"/departments/")

    assert response.status_code == 200
    response = json.loads(response.content)
    assert len(response) == 2


def test_department_viewset_create(db):
    department = {
        "company": {
            "name": "Company",
            "cnpj": "21342121245322",
            "address": "Rua",
            "city": "Rio de Jáneiro",
            "state": "RJ",
            "country": "Brasil"
        },
        "cost_center": {
            "company": {
                "name": "Company",
                "cnpj": "21342121245322",
                "address": "Rua",
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
    }

    user = baker.make(User)

    data = json.dumps(department)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/departments/", data, content_type='application/json')

    assert response.status_code == 201
    
    departments = Department.objects.all()
    
    assert len(departments)


def test_department_viewset_update(db):
    baker.make(Department, name="Tecnologia")
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    query_department = Department.objects.all().values()[0]

    assert query_department['name'] == 'Tecnologia'

    updated_department = {
        "name": "Computação"
    }

    response = client.put(f"/departments/{query_department['id']}/", updated_department)

    query_department = Department.objects.all().values()[0]

    assert query_department['name'] == updated_department['name']
    assert response.status_code == 200


def test_cost_center_viewset_destroy(db):
    baker.make(Department)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
 
    query_department = Department.objects.all().values()[0]

    response = client.delete(f"/departments/{query_department['id']}/")

    query_department = Department.objects.all()

    assert response.status_code == 204
    assert not len(query_department)


def test_department_viewset_list_not_authenticated(db):
    department = baker.make(Department, name="Tecnologia")

    user = baker.make(User)

    client = APIClient()

    response = client.get("/departments/")

    assert response.status_code == 403


def test_department_simple_list_ordered(db):
    department1 = baker.make(Department, name="Wtecnologia")
    department2 = baker.make(Department, name="Ytecnologia")
    department3 = baker.make(Department, name="Atecnologia")
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/departments/?ordering=name")

    assert response.status_code == 200
    response = json.loads(response.content)
    
    assert department3.name == response[0]['name'] # department3.name = Acartão 1º
    assert department1.name == response[1]['name'] # department1.name = Wcartão 2º
    assert department2.name == response[2]['name'] # department2.name = Ycartão 3º


def test_department_simple_list_search(db):
    department = baker.make(Department, name="Wtecnologia")
    baker.make(Department, _quantity=6)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    all_active_departments = Department.objects.all()

    assert len(all_active_departments) == 7

    response = client.get("/departments/?search=Wtecnologia")

    assert response.status_code == 200
    response = json.loads(response.content)

    assert len(response) == 1
    assert response[0]['name'] == "Wtecnologia"


def test_department_simple_list_pagination(db):
    PAGE_SIZE = 10
    baker.make(Department, _quantity=20)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/departments/?page=1")
    assert response.status_code == 200
    response = json.loads(response.content)

    assert len(response) == PAGE_SIZE
