# people_platform_backend
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
- [Flake8][https://flake8.pycqa.org/en/latest/] = utilizando o arquivo setup.cfg que tem regras específicas sobre as configurações do projeto.
- [Django_extensions][https://django-extensions.readthedocs.io/en/latest/] = Adiciona diversas ferramentas que você pode utilizar durante o desenvolvimento, uma delas é o shell_plus `python manage.py shell_plus`, semelhante ao shell normal, porém irá realizar o importe dos models automaticamente para você[
- [Pytest-django][https://pytest-django.readthedocs.io/en/latest/] = Utilizado para criação de testes unitários que garantem a funcionalidade do código.
- [Model_bakery][https://model-bakery.readthedocs.io/en/latest/] = Facilita a criação de objetos no banco, assim, agilizando a velocidade de desenvolvimento.
