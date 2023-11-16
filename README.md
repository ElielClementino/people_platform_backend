# People Platform Backend
Backend de uma plataforma de cadastro de funcionários. Feito utilizando django e django rest framework.

## Setup do projeto
Primeiramente é necessário modificar o nome do arquivo .env-example para .env pois é nesse arquivo que se encontra ar váriaveis do projeto.  
`$ cp .env-example .env`  
Após ter modificado o arquivo .env-examplo para .env, podemos rodar o projeto de duas formas:  
### Docker:
1. No terminal rode  
`$ docker-compose up`  
2 serviços serão iniciados **backend** e **postgres**, primeiro será criado a imagem do backend utilizando a dockerfile como contexto, após isso, o serviço do postgres também será inicializado, caso você já possua a imagem do postgres presente no arquivo docker-compose.yml ele já irá inicializar o serviço, caso não, ela tentará encontrar a imagem e fará o pulling.  
2. Após isso você pode conferir se os dois serviços estão de pé com o comando `$ docker ps`, estando os 2 serviços de pé, você pode acessar a url: http://localhost:8000.  
Caso queira acessar o container para utilização de comandos ou uso do shell, você pode uilizar o comando `$ docker exec -it IDDOCONTAINER bash`,  assim você irá entrar no container no modo interativo e poderá utilizar o manager do django.  
### Pip:
As dependências do projeto se encontram no arquivos **requirements.txt** e **requirements-dev.txt**.
1. Instale as dependências do projeto usando o seguinte comando:
`$ pip install -r requirements-dev.txt`
Esse comando irá instalar as dependências de desenvolvimento do projeto e logo após as depêndencias para rodar o projeto.  
2. Será necessário subir o container do postgres, para isso, rode no terminal o seguinte comando:
`$ docker-compose up postgres`
3. Após ter baixado as dependências do projeto, e subido o container do postgres, você irá subir o server, com o seguinte comando:
`$ python manage.py runserver`
## Plugins presente no projeto:
- [Flake8](https://flake8.pycqa.org/en/latest/) = utilizando o arquivo setup.cfg que tem regras específicas sobre as configurações do projeto.
- [Django_extensions](https://django-extensions.readthedocs.io/en/latest/) = Adiciona diversas ferramentas que você pode utilizar durante o desenvolvimento, uma delas é o shell_plus `python manage.py shell_plus`, semelhante ao shell normal, porém irá realizar o importe dos models automaticamente para você[
- [Pytest-django](https://pytest-django.readthedocs.io/en/latest/) = Utilizado para criação de testes unitários que garantem a funcionalidade do código.
- [Model_bakery](https://model-bakery.readthedocs.io/en/latest/) = Facilita a criação de objetos no banco, assim, agilizando a velocidade de desenvolvimento.

# Endpoints:

## Accounts

### `/whoami`:
method: ['GET']  
Retorna informações sobre o usuário, se está logado e permissões,.
Exemplo de JSON de saída:
```json
# Usuário autenticado Ex:
user_dict_info = {
        "id": 1,
        "name": Usuario nome,
        "username": Usuario,
        "first_name": Usuario,
        "last_name": nome,
        "email": usuario@gmail.com,
        "permissions": {
            "ADMIN": true,
            "STAFF": true,
        },
    "authenticated": true
}
```
```json
# Usuário não autenticado
user_dict_info = {
    "authenticated": false
}
```
### `/login`:
 method: ['POST']  
 Faz login com base na senha e usuário.
 Parâmetros:  
    username(str)
    password(str)

### `/logout`:
method: ['POST']  
Faz logout quando chama o endpoint, não precisa de parâmetros.

### `register`:
method: ['POST']  
Registra o usuário no banco de dados.
Exemplo JSON de entrada:  
```json
new_user = {"userInfo": { "username": "user", "email":"user@example.com", "password": "user"}}
```
## Core

### /companies/:
methods: ['GET', 'POST'].
Lista dados sobre a empresa e permite cadastrar novas empresas.
> Parâmetros POST:
> - name(str)
> - cnpj(str)
> - address(str)
> - city(str)
> - state(str)
> - country(str)
Exemplo JSON de saída:  
```json
#GET
{
        "name": "Company",
        "cnpj": "21342121245322",
        "address": "Rua",
        "city": "Rio de Jáneiro",
        "state": "RJ",
        "country": "Brasil"
},
```
### /companies/<int: pk>
methods: ['PUT', 'DELETE'].  
É possível atualizar os dados da empresa utilizando PUT, e apagar alguma empresa usando DELETE.
```json
# PUT
{
        "name": "Empresa",
        "cnpj": "21342121245322",
        "address": "Rua",
        "city": "Rio de Jáneiro",
        "state": "RJ",
        "country": "Brasil"
},
```
### /cost_centers/:
methods: ['GET', 'POST'].  
Lista os centros de custo de cada empresa, e permite criar um centro de custo atrelado a uma empresa.  
> Parâmetros POST:
> - company(fk) - A qual empresa esse centro pertence
> - code(str) - Código de identificação do centro de custo
> - description(str) - Nome do centro de custo
> - cost(str) - Custos atrelado a esse centro
Exemplo JSON de saída:
```json
#GET
{
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
```
### /cost_centers/<int: pk>
methods: ['PUT', 'DELETE'].  
Utilizando eses 2 métodos você pode tanto atualizar quanto deletar um centro de custos.
```json
# PUT
{
        "name": "Empresa",
        "cnpj": "21342121245322",
        "address": "Rua",
        "city": "Rio de Jáneiro",
        "state": "RJ",
        "country": "Brasil"
},
```

### /departments/>
methods: ['GET', 'POST'].  
Com o get é retornado dados sobre os departamentos e quais dados estão atrelados a isso, como 'centro de custo' e 'empresa'. E o Post faz a criação desses departamentos.  
> Parâmetros POST:
> - company(fk) - A qual empresa esse centro pertence
> - cost_center(fk) - A qual centro de custo o departamento está atrelado
> - name(str) - Nome do departamento
> - integration_code(str) - Código de integração
Exemplo JSON de saída:  
```json
# GET
{
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
    },
```
### /departments/<int: pk>
methods: ['PUT', 'DELETE'].  
Utilizando eses 2 métodos você pode tanto atualizar quanto deletar um centro de custos.
```json
# PUT
{
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
        "integration_code": "26"
    },
```
### /employees/>
methods: ['GET', 'POST'].  
Com o get é retornado dados sobre os colaboradores, como, em qual empresa, e depertamento fazem parte. Com os post é possível atrelar colaboradores  a empresas cadastradas no sistema.
> Parâmetros POST:
> - company(fk) - A qual empresa esse colaborador faz parte.
> - department(fk) - A qual departamento esse colaborador faz parte.
> - full_name(str) - Nome completo do colaborador
> - email(str) - Email válido do colaborador
> - phone_number - Número de telefone do colaborador
> - birth_date - Data de nascimento do colaborador
> - entry_date - Data de entrada do colaborador na empresa
> - departure_date - Data de desligamento do colaborador
> - city - De qual cidade o colaborador vem.
Exemplo JSON de saída:  
```json
# GET
{
        "company": {
            "name": "Company",
            "cnpj": "21342121245322",
            "address": "Rua",
            "city": "Rio de Jáneiro",
            "state": "RJ",
            "country": "Brasil"
        },
        "department": {
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
            "integration_code": "26"
        },
        "full_name": "User Name",
        "email": "User@gmail.com",
        "phone_number": "(21)462159684",
        "birth_date": "1998-01-28",
        "entry_date": "2023-11-14",
        "departure_date": null,
        "city": "Rio de Jáneiro"
    },
```
### /employees/<int: pk>
methods: ['PUT', 'DELETE'].  
Utilizando esses 2 métodos você pode tanto atualizar quanto deletar informações sobre um colaborador.
```json
# PUT

{
    "company": {
        "name": "Company",
        "cnpj": "21342121245322",
        "address": "Rua",
        "city": "Rio de Jáneiro",
        "state": "RJ",
        "country": "Brasil"
    },
    "department": {
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
        "integration_code": "26"
    },
    "full_name": "UserName",
    "email": "Username@gmail.com",
    "phone_number": "(21)462159684",
    "birth_date": "1998-01-28",
    "entry_date": "2023-11-14",
    "departure_date": null,
    "city": "Rio de Jáneiro"
},
```
## Search, Ordering e Pagination
### `Search`  
É possível realizar essa busca passando o parâmetro 'search' na url http://localhost:8000/employees/?search=company
logo, será filtrado as empresas com o nome de 'company' 
### Company
> ('name', 'cnpj')
### CostCenter
> ('company__name', 'code', 'description')
### Department
>  ('company__name', 'name', 'integration_code')  
### Employee
> ('full_name', 'email', 'city')  
### `Ordering`  
Para ordenar os dados basta passar na url o parâmetro 'ordering' na url http://localhost:8000/employees/?order=full_name.  
Assim, irá ordernar os colaboradores pelo nome completo  
### `Pagination`
Os dados irão retornar no máximo de 10 em 10 objetos por página, portanto, para ver a próxima página é necessário passar na url o seguinte parâmetro
 http://localhost:8000/employees/?page=2
