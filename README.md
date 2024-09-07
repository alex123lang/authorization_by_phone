
# Реферальное приложение API

Этот проект реализует API реферальной системы с регистрацией пользователей, аутентификацией через SMS-коды и отслеживанием использования инвайт-кодов. Проект создан с использованием Django и Django REST Framework, а для аутентификации используется JWT. Ниже приведены инструкции по настройке, тестированию и использованию API.

## Функционал
- Регистрация пользователей по номеру телефона
- Аутентификация через SMS-код
- Генерация инвайт-кодов
- Отслеживание использования инвайт-кодов
- Аутентификация через JWT

## Требования

- Python 3.x
- Django
- Django REST Framework
- djangorestframework-simplejwt

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/alex123lang/referral-app.git
    ```
    
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Примените миграции базы данных:
    ```bash
    python manage.py migrate
    ```

4. Создайте суперпользователя (необязательно):
    ```bash
    python manage.py csu
    ```

5. Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```

## Эндпоинты API

### 1. Регистрация нового пользователя

**POST** `register/`

- Пример тела запроса (JSON):
    ```json
    {
      "phone_number": "79999999999"
    }
    ```

- Пример успешного ответа:
    ```json
    {
      "phone_number": "79999999999",
      "invite_code": "DEF456",
      "invite_used": null
    }
    ```

### 2. Авторизация пользователя

**POST** `login/`

- Пример тела запроса (JSON):
    ```json
    {
      "phone_number": "79999999999",
      "auth_code": "1234"
    }
    ```

- Пример успешного ответа:
    ```json
    {
      "refresh": "<refresh_token>",
      "access": "<access_token>"
    }
    ```

### 3. Получение профиля пользователя

**GET** `<user_id>/`

- Пример успешного ответа:
    ```json
    {
      "phone_number": "79999999999",
      "invite_code": "DEF456",
      "invite_used": "",
      "users_with_my_invite_code": []
    }
    ```

### 4. Обновление кода подтверждения, если пользователь уже был зарегистрирован

**PUT** `/api/<user_id>/auth_code_update/`

- Пример тела запроса (JSON):
    ```json
    {
      "phone_number": "79999999999"
    }
    ```

- Пример успешного ответа:
    ```json
    {
      "phone_number": "79999999999",
      "invite_code": "DEF456",
      "invite_used": null
    }
    ```

### 5. Обновление токена

**POST** `/api/token/refresh/`

- Пример тела запроса (JSON):
    ```json
    {
      "refresh": "<refresh_token>"
    }
    ```

- Пример успешного ответа:
    ```json
    {
      "access": "<new_access_token>"
    }
    ```

## Запуск тестов

В проекте включены тесты для ключевого функционала, включая регистрацию, авторизацию и получение профиля. Для запуска тестов выполните команду:

```bash
python manage.py test
```

Чтобы проверить покрытие тестами:

1. Установите `coverage`:
    ```bash
    pip install coverage
    ```

2. Запустите тесты с проверкой покрытия:
    ```bash
    coverage run --source='referral_app' manage.py test
    ```

3. Посмотрите отчет о покрытии:
    ```bash
    coverage report -m
    ```

## Коллекция Postman

Коллекция запросов Postman предоставлена для удобства тестирования всех эндпоинтов API. Вы можете импортировать коллекцию в Postman, используя JSON файл

