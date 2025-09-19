## Инициализация базы данных
```bash
bash build/create_database_psql.sh
```
> Создает базу данных по умолчанию и заполняет ее данными из файла app/core/database/schema.sql
> Указывает пароль для базы данных в файле .create_user.log

<br>

## Diagram of Universal Database
![img](Diagram_of_Universal_Database_ordered.png)

## Генерация моделей для SQLAlchemy из схемы базы данных
```bash
python -m sqlacodegen --generator sqlmodels --outfile app/core/database/models.py 'postgresql+psycopg://universal:$UNIVERSAL_DB_PASSWORD@localhost:5432/universal'
```

<br>

## Пример конфигурационного файла .env
```
DEBUG=False

PG_HOST=localhost
PG_PORT=5432
PG_USER=universal
PG_DBNAME=universal
PG_PASSWORD=password

JWT_SECRET_KEY = '123'
```

<br>

## Генерация данных для тестирования БД
```bash
python -m build.generate_data
```

<br>

## Запуск сервера
```bash
python -m app.main
```

## Запуск сервера в режиме разработки
```bash
python -m uvicorn app.main:app --reload
```

<br>


## Endpoints

```bash
/docs # Swagger UI
/health # Check server status
```
