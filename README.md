![foodgram_workflow](https://github.com/AleksandrTka4uk/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)

# foodgram-project
Проект foodgram-project собирает позволяет пользователям публиковать рецепты.
Пользователь может выбрать рецепты и скачать список ингредиентов, которые необходимы
для их приготовления.

## Требования
Для старта проекта необходимо установить Docker.

## Настройка окружения
Перед запуском проекта необходимо настроить окружение. 
Создайте файл **.env** с переменными окружения на основе файла **.env.example**

## Запуск приложения

Для запуска приложения выполните команду:

 ``` 
docker-compose up
 ``` 

Залогинитесь в контейнер web:
 ``` 
docker-compose exec web sh
 ``` 
В контейнере выполните команды:
 ``` 
python manage.py migrate --noinput 
python manage.py collectstatic --no-input 
 ``` 
Для создания суперпользователя выполните команду:
 ``` 
python manage.py createsuperuser 
 ``` 

Для наполнения базы данными ингредиентов распакуйте файл **ingredients.csv** 
в директорию проекта. Выполните команду:

```
python manage.py import_ingredients_csv
python manage.py import_tags_csv
```

## Технологии
В проекте используются технологии:

- [Django==3.2.2](https://www.djangoproject.com/)
- [django-debug-toolbar==3.2.1](https://django-debug-toolbar.readthedocs.io/en/latest/)
- [django-filter==2.4.0](https://django-filter.readthedocs.io/en/stable/)
- [django-pdfkit==0.3.1](https://django-pdfkit.readthedocs.io/en/latest/)
- [djangorestframework==3.12.4](https://www.django-rest-framework.org/)
- [docker==5.0.0](https://docs.docker.com/)
- [docker-compose==1.29.2](https://docs.docker.com/)
- [factory-boy==3.2.0](https://factoryboy.readthedocs.io/)
- [Faker==8.10.1](https://faker.readthedocs.io/en/master/)
- [gunicorn==20.1.0](https://gunicorn.org/)
- [pdfkit==0.6.0](https://pdfkit.org/)
- [Pillow==8.2.0](https://pillow.readthedocs.io/)
- [python-dotenv==0.18.0](https://pypi.org/project/python-dotenv/)
- [requests==2.26.0](https://docs.python-requests.org/)
- [sorl-thumbnail==12.7.0](https://sorl-thumbnail.readthedocs.io/en/latest/)
- [nginx==1.19.3](https://nginx.org/ru/)
- [postgres:12.4](https://www.postgresql.org/)
- [django-more-admin-filters==1.3](https://github.com/thomst/django-more-admin-filters)

## Об авторе
Ткачук Александр Валерьевич. Студент 10 когорты Яндекc.Практикум.
[GitHub](https://github.com/AleksandrTka4uk/)

## Лицензия
Проект лицензируется по [лицензии MIT](https://opensource.org/licenses/MIT)
