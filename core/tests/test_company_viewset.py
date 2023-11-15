import json

from model_bakery import baker, seq
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from core.models import Company
from core.viewsets import CompanyViewSet

def test_company_viewset_list_(db):
    companies = baker.make(Company, name=seq("company"), _quantity=2)

    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/companies/")

    assert response.status_code == 200
    response = json.loads(response.content)

    assert len(response) == 2


def test_company_viewset_create(db):
    company = {
        'name': 'companyTeste',
        'cnpj': '0123456789123',
        'address': 'Bonsucesso',
        'city': 'Rio de Janeiro',
        'state': 'RJ',
        'country': 'Brasil',
    }
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
 
    response = client.post("/companies/", company)

    query_company = Company.objects.all().values()[0]

    assert response.status_code == 201
    assert response.data['cnpj'] == query_company['cnpj']


def test_company_viewset_update(db):
    company = {
        'name': 'companyTeste',
        'cnpj': '0123456789123',
        'address': 'Bonsucesso',
        'city': 'Rio de Janeiro',
        'state': 'RJ',
        'country': 'Brasil',
    }
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
 
    response = client.post("/companies/", company)

    query_company = Company.objects.all().values()[0]

    assert response.status_code == 201
    assert response.data['cnpj'] == query_company['cnpj']

    updated_company = {
        'name': 'companyTeste',
        'cnpj': '7891230123456',
        'address': 'Bonsucesso',
        'city': 'Rio de Janeiro',
        'state': 'RJ',
        'country': 'Brasil',
    }
    response = client.put(f"/companies/{query_company['id']}/", updated_company)

    query_updated_company = Company.objects.all().values()[0]

    assert response.status_code == 200
    assert response.data['cnpj'] != query_company['cnpj']
    assert response.data['cnpj'] == query_updated_company['cnpj']


def test_company_viewset_create(db):
    company = {
        'name': 'companyTeste',
        'cnpj': '0123456789123',
        'address': 'Bonsucesso',
        'city': 'Rio de Janeiro',
        'state': 'RJ',
        'country': 'Brasil',
    }
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
 
    response = client.post("/companies/", company)

    query_company = Company.objects.all().values()[0]

    assert response.status_code == 201
    assert response.data['cnpj'] == query_company['cnpj']


def test_company_viewset_destroy(db):
    baker.make(Company)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)
 
    query_company = Company.objects.all().values()[0]

    response = client.delete(f"/companies/{query_company['id']}/")

    query_company = Company.objects.all()

    assert response.status_code == 204
    assert not len(query_company)


def test_company_viewset_list_not_authenticated(db):
    companies = baker.make(Company, name=seq("company"), _quantity=2)

    user = baker.make(User)

    client = APIClient()

    response = client.get("/companies/")

    assert response.status_code == 403


def test_company_simple_list_ordered(db):
    company1 = baker.make(Company, name="Zcompany")
    company2 = baker.make(Company, name="Acompany")
    company3 = baker.make(Company, name="Fcompany")
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/companies/?ordering=name")

    assert response.status_code == 200
    response = json.loads(response.content)
    
    assert company2.name == response[0]['name'] # company2.name = Acompany 1º
    assert company3.name == response[1]['name'] # company3.name = Fcompany 2º
    assert company1.name == response[2]['name'] # company1.name = Zcompany 3º


def test_company_simple_list_search(db):
    company1 = baker.make(Company, name="Zcompany")
    baker.make(Company, _quantity=6)
    user = baker.make(User)

    client = APIClient()
    client.force_authenticate(user=user)

    all_active_companies = Company.objects.all()

    assert len(all_active_companies) == 7

    response = client.get("/companies/?search=Zcompany")

    assert response.status_code == 200
    response = json.loads(response.content)

    assert len(response) == 1
    assert response[0]['name'] == "Zcompany"

