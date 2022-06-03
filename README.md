# CI и CD проекта api_yamdb ![Action status](https://github.com/Andrey-Vyshegorodskiy/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## yamdb_final
### Описание

Ссылка на сайт:

http://84.201.141.50/admin/

http://84.201.141.50/api/v1/

http://84.201.141.50/redoc/

Разработка:
- :white_check_mark: [Andrey-Vyshegorodskiy](https://github.com/Andrey-Vyshegorodskiy)

Полная документация к API находится в http://84.201.141.50/redoc/
### Технологии
Python 3.7, Django 2.2, DRF, JWT, docker

### Примеры работы с API для всех пользователей
Подробная документация доступна по адресу /redoc/
Для неавторизованных пользователей работа с API доступна в режиме чтения,
что-либо изменить или создать не получится. 

Права доступа: Доступно без токена.
```
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
```
Права доступа: Администратор
```
GET /api/v1/users/ - Получение списка всех пользователей
GET /api/v1/users/{username}/  - Получение пользователя по username
```

### Виды пользователей
- Анонимный пользователь — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — помимо прав доступа Анонимного пользователя, дополнительно может публиковать отзывы и ставить оценку произведениям, комментировать чужие отзывы; кроме того может редактировать и удалять свои отзывы и комментарии. Присваивается автоматически каждому новому пользователю.
- Модератор (moderator) — помимо прав доступа Аутентифицированного пользователя имеет право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом. Может создавать и удалять произведения, категории и жанры, назначать роли пользователям.

### Регистрация нового пользователя

Регистрация нового пользователя:
```
POST /api/v1/auth/signup/
{
  "email": "string",
  "username": "string"
}
```
Поля email и username должны быть уникальными.

Получение JWT-токена:
```
POST /api/v1/auth/token/
{
  "username": "string",
  "confirmation_code": "string"
}
```

### Примеры работы с API для авторизованных пользователей
- Права доступа: admin.

Добавление категории:
```
POST /api/v1/categories/
{
  "name": "string",
  "slug": "string"
}
```

Удаление категории:
```
DELETE /api/v1/categories/{slug}/
```

Добавление жанра:
```
POST /api/v1/genres/
{
  "name": "string",
  "slug": "string"
}
```

Удаление жанра:
```
DELETE /api/v1/genres/{slug}/
```

Добавление произведения:
```
POST /api/v1/titles/
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Год выпуска произведения не может быть больше текущего.

Частичное обновление информации о произведении:
```
PATCH /api/v1/titles/{titles_id}/
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Удаление произведения:
```
DELETE /api/v1/titles/{titles_id}/
```

- Права доступа: user.

Создание отзыва на произведение:
```
POST /api/v1/titles/{title_id}/reviews/
{
  "text": "string",
  "score": 1
}
```

Частичное обновление отзыва:
```
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/
{
  "text": "string",
  "score": 1
}
```

Удаление отзыва:
```
DELETE /api/v1/titles/{title_id}/reviews/{review_id}/
```