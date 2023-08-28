# Foodgram
### Описание проекта

Foodgram — это сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд. Список покупок доступен к скачиванию.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:VanGogh77/foodgram-project-react.git
```

```
cd foodgram-project-react/backend
```
Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:

```
(venv) $ python -m pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Загрузить статику:

 ```
 (venv) $ python manage.py collectstatic
 ```
Загрузить список ингредиентов:
```
python manage.py load_ingredients
```

Запустить сервер:

 ```
 (venv) $ python manage.py runserver
 ```

## Ссылка на сайт:
https://goatfoodgram.servequake.com

## Информация об авторе:
https://github.com/VanGogh77
