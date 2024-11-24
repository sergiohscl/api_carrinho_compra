# Projeto Django Reste Framework (api_carrinho_compra)

## Objetivo do projeto e colocar em prática os meus conhecimentos em criar apis e fazer testes unitários.

## Documentação do django
https://www.djangoproject.com/

## Instalando ambiente virtual
    python3 -m venv venv

## Instale as dependências no projeto
    pip install -r requirements.txt

## Migrando a base de dados do Django
    python manage.py makemigrations
    python manage.py migrate

## Criando e modificando a senha de um super usuário
    python manage.py createsuperuser
    python manage.py changepassword USERNAME

## Rodando django-admin
    python manage.py runserver


# Rodando projeto em Docker

## Buildar a imagem
    docker build -t api-carrinho-image .

## Rodar o container com a imagem da aplicação
    docker run --name api-carrinho-container -p 8000:8000 api-carrinho-image

## Acessar container
    docker exec -it api-carrinho-container /bin/bash