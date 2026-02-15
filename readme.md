# README

## Запуск бота

1. Перейти в папку с проектом в терминале.

2. Создать виртуальное окружение:
```bash
python -m venv venv
```

3. Активировать виртуальное окружение:

**Для Windows:**
```bash
.\venv\Scripts\Activate
```

**Для Linux / Debian:**
```bash
source venv/bin/activate
```

4. Установить зависимости:
```bash
pip install -r requirements.txt
```

5. Создать файл конфигурации `.env` на основе примера `config.example.env` и заполнить нужные ключи (например, токен бота, данные базы данных).

6. Запуск приложения (API):
```bash
uvicorn api.app:app --reload
```

Приложение будет доступно по адресу `http://127.0.0.1:8000`.


## Назначение роли суперадмина в PostgreSQL

Чтобы назначить пользователя суперадмином, нужно выполнить следующие SQL-запросы в базе данных PostgreSQL:

```sql
UPDATE users
SET role = 'super_admin'
WHERE tg_id = 123456789;
```
*Замените `123456789` на ID пользователя, которому нужно дать права.*

## Установка PostgreSQL и подключение

### Установка PostgreSQL в терминале (Linux / Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Подключение к базе через psql:
```bash
psql -U имя_пользователя -d имя_базы
```
Далее будет запрошен ваш пароль для базы (при вводе он будет скрыт).

