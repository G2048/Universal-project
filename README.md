## Инициализация базы данных
```bash
bash create_database_psql.sh
```
> Создает базу данных по умолчанию и заполняет ее данными из файла app/core/database/schema.sql
> Указывает пароль для базы данных в файле .create_user.log


## Генерация моделей для SQLAlchemy из схемы базы данных
```bash
python -m sqlacodegen --generator sqlmodels --outfile app/core/database/models.py 'postgresql+psycopg://universal:$UNIVERSAL_DB_PASSWORD@localhost:5432/universal'
```
