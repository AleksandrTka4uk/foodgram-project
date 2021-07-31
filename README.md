![foodgram_workflow](https://github.com/AleksandrTka4uk/foodgram-project/actions/workflows/foodgram_workflow.yml.yml/badge.svg)

# foodgram-project
Проект foodgram-project собирает позволяет пользователям публиковать рецепты.
Пользователь может выбрать рецепты и скачать список ингредиентов, которые не обходимы
для их приготовления.

## Требования
Для старта проекта необходимо установить Docker.

## Настройка окружения
Перед запуском проекта необходимо настроить окружение. 
Создайте файл .env с переменными окружения на основе файла .env.example

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

Для наполнения базы данными ингредиентов распакуйте файл ingredients.csv` 
в директорию проекта. Выполните команду:

```
python manage.py import_ingredients_csv
python manage.py import_tags_csv
```

## Технологии
В проекте используются технологии:


## Об авторе
Ткачук Александр Валерьевич. Студент 10 когорты Яндекc.Практикум.
[GitHub](https://github.com/AleksandrTka4uk/)

## Лицензия
Проект лицензируется по [лицензии MIT](https://opensource.org/licenses/MIT)