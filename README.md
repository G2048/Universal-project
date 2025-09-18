## Инициализация базы данных
```bash
bash build/create_database_psql.sh
```
> Создает базу данных по умолчанию и заполняет ее данными из файла app/core/database/schema.sql
> Указывает пароль для базы данных в файле .create_user.log

<br>

## Генерация моделей для SQLAlchemy из схемы базы данных
```bash
python -m sqlacodegen --generator sqlmodels --outfile app/core/database/models.py 'postgresql+psycopg://universal:$UNIVERSAL_DB_PASSWORD@localhost:5432/universal'
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
