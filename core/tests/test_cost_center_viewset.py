import json

from model_bakery import baker, seq
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from core.models import CostCenter, Company

def test_cost_center_viewset_list_(db):
    company = baker.make(Company, name="Test_company")
    cost_centers = baker.make(CostCenter, company=company, description=seq("Cartão"), _quantity=2)

    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(f"/cost_centers/")

    assert response.status_code == 200
    response = json.loads(response.content)
    assert len(response) == 2


def test_cost_center_viewset_create(db):
    company = baker.make(Company, name="Test_company")
    cost_center = { 
        'company': {
        'name': 'Test_company', 'cnpj':'1234567777843',
        'address':'rua', 'city':'Rio de Janeiro',
        'state':'RJ', 'country':'Brazil'
        },
        'code': '22', 'description': 'Cartão', 'cost': 222.22 }
    user = baker.make(User)

    data = json.dumps(cost_center)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post("/cost_centers/", data, content_type='application/json')

    assert response.status_code == 201
    
    cost_centers = CostCenter.objects.all()
    
    assert len(cost_centers)


def test_cost_center_viewset_update(db):
    baker.make(CostCenter, description="Cartão1")
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    query_cost_center = CostCenter.objects.all().values()[0]

    assert query_cost_center['description'] == 'Cartão1'

    updated_cost_center = {
        "description": "Cartão2"
    }

    response = client.put(f"/cost_centers/{query_cost_center['id']}/", updated_cost_center)

    query_cost_center = CostCenter.objects.all().values()[0]

    assert query_cost_center['description'] == updated_cost_center['description']
    assert response.status_code == 200


def test_cost_center_viewset_destroy(db):
    company = baker.make(Company)
    baker.make(CostCenter, company=company)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
 
    query_cost_center = CostCenter.objects.all().values()[0]

    response = client.delete(f"/cost_centers/{query_cost_center['id']}/")

    query_cost_center = CostCenter.objects.all()

    assert response.status_code == 204
    assert not len(query_cost_center)


def test_cost_center_viewset_list_not_authenticated(db):
    cost_center = baker.make(CostCenter, description="Cartão")

    user = baker.make(User)

    client = APIClient()

    response = client.get("/cost_centers/")

    assert response.status_code == 403


def test_cost_center_simple_list_ordered(db):
    cost_center1 = baker.make(CostCenter, description="Wcartão")
    cost_center2 = baker.make(CostCenter, description="Ycartão")
    cost_center3 = baker.make(CostCenter, description="Acartão")
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/cost_centers/?ordering=description")

    assert response.status_code == 200
    response = json.loads(response.content)
    
    assert cost_center3.description == response[0]['description'] # company2.description = Acartão 1º
    assert cost_center1.description == response[1]['description'] # company3.description = Wcartão 2º
    assert cost_center2.description == response[2]['description'] # company1.description = Ycartão 3º


def test_cost_center_simple_list_search(db):
    cost_center1 = baker.make(CostCenter, description="Wcartão")
    baker.make(CostCenter, _quantity=6)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    all_active_cost_centers = CostCenter.objects.all()

    assert len(all_active_cost_centers) == 7

    response = client.get("/cost_centers/?search=Wcartão")

    assert response.status_code == 200
    response = json.loads(response.content)

    assert len(response) == 1
    assert response[0]['description'] == "Wcartão"


def test_cost_center_simple_list_pagination(db):
    PAGE_SIZE = 10
    baker.make(CostCenter, _quantity=20)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/cost_centers/?page=1")
    assert response.status_code == 200
    response = json.loads(response.content)

    assert len(response) == PAGE_SIZE