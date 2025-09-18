from datetime import datetime

import pytz
from faker import Faker
from sqlmodel import Session, create_engine, text

from app.configs import get_database_settings
from app.core.database.models import Companies

from .ru_facker import RussianBusinessProvider

db_settings = get_database_settings()
engine = create_engine(db_settings.pg_dsn)


def fill_company_data(companies: list[Companies]):
    print()
    print("Fill Companies data...")

    with Session(engine) as session:
        for company in companies:
            print(f"Insert {company.name}")
            session.add(company)
        session.commit()


def generate_test_company_data():
    fake = Faker("ru_RU")
    fake.add_provider(RussianBusinessProvider)
    companies_data = []
    count_of_rows = 10
    for _ in range(count_of_rows):
        company_type = fake.russian_company_type()
        companies_data.append(
            Companies(
                property_id=1,
                name=str(fake.russian_company_name(company_type)),
                inn=str(fake.russian_inn()),
                kpp=str(fake.russian_kpp()),
                ogrn=str(fake.russian_ogrn()),
                bic=str(fake.random_int(100000000, 999999999)),
            )
        )

    assert companies_data != []
    print(list(map(lambda c: (c.name), companies_data)))
    fill_company_data(companies_data)


def generate_timezone_dict():
    print()
    print("Fill timezone_dict data...")

    with Session(engine) as session:
        for tz_name in pytz.all_timezones:
            try:
                _timezone = pytz.timezone(tz_name)
                utc_now = datetime.utcnow()
                # Localize the UTC time to the specific timezone
                local_time = pytz.utc.localize(utc_now).astimezone(_timezone)
                # print(f"{tz_name}:{local_time.strftime('%z')}")
                print(f"{tz_name}:{local_time}")
            except pytz.UnknownTimeZoneError:
                print(f"Could not process timezone: {tz_name}")

            # Warning: insert via model occurs incorrect timezone
            # timezone_dict = TimezoneDict(
            #     timezone_name=tz_name,
            #     timezone=local_time,
            # )
            # print(f"{timezone_dict}")
            timezone_dict = text(
                f"INSERT INTO timezone_dict (timezone_name, timezone) VALUES ('{tz_name}','{local_time}');"
            )
            session.execute(timezone_dict)
        session.commit()


def generate_roles_dict():
    print()
    print("Fill roles_dict data...")
    sql_insert = """INSERT INTO roles_dict (code, name) VALUES
    ('admin', 'Администратор'),
    ('user', 'Обычный пользователь'),
    ('moderator', 'Модератор'),
    ('guest', 'Гость'),
    ('developer', 'Разработчик'),
    ('support', 'Служба поддержки'),
    ('manager', 'Менеджер'),
    ('auditor', 'Аудитор');
    """
    sql_select = "SELECT * FROM roles_dict;"
    with Session(engine) as session:
        session.exec(text(sql_insert))
        session.commit()
        roles = session.exec(text(sql_select)).fetchall()
    print(f"{roles=}")


def generate_settings_dict():
    print()
    print("Fill settings_dict data...")
    sql_insert = """
    INSERT INTO settings_dict (code, name) VALUES
    ('system_timeout', 'Время ожидания сессии (секунд)'),
    ('max_login_attempts', 'Максимальное число попыток входа'),
    ('enable_logging', 'Включить журналирование'),
    ('password_min_length', 'Минимальная длина пароля'),
    ('session_lifetime', 'Время жизни сессии (миллисекунды)'),
    ('default_language', 'Язык по умолчанию'),
    ('allow_guest_access', 'Разрешить доступ гостям'),
    ('maintenance_mode', 'Режим обслуживания'),
    ('max_upload_size', 'Максимальный размер загружаемого файла (МБ)'),
    ('api_rate_limit', 'Ограничение числа запросов к API');
    """
    sql_select = "SELECT * FROM settings_dict;"
    with Session(engine) as session:
        session.exec(text(sql_insert))
        session.commit()
        roles = session.exec(text(sql_select)).fetchall()
    print(f"{roles=}")


def generate_settings():
    print()
    print("Fill settings data...")
    sql_insert = """
    INSERT INTO settings (setting_code_id, value, active_from, active_to) VALUES
    (1, '300', '2024-01-01', NULL),
    (2, '5', '2023-11-01', '2024-12-31'),
    (3, 'true', '2023-01-01', NULL),
    (4, '8', '2024-05-01', NULL),
    (5, '1800000', '2024-01-01', '2025-01-01'),
    (6, 'ru', '2023-01-01', NULL),
    (7, 'false', '2024-03-01', '2024-10-01'),
    (8, 'true', '2024-01-01', NULL),
    (9, '50', '2023-06-01', NULL),
    (10, '1000', '2024-01-01', '2024-12-31');
    """
    sql_select = "SELECT * FROM settings;"
    with Session(engine) as session:
        session.exec(text(sql_insert))
        session.commit()
        roles = session.exec(text(sql_select)).fetchall()
    print(f"{roles=}")


def generate_functions_dict():
    print()
    print("Fill functions_dict data...")
    sql_insert = """
    INSERT INTO functions_dict (id, code, version) VALUES
    (1, 'manage_all', 1),
    (2, 'delete_users', 1),
    (3, 'list_users', 1),
    (4, 'manage_users', 1),
    (5, 'manage_companies', 2),
    (6, 'manage_settings', 1),
    (7, 'manage_groups', 1),
    (8, 'manage_roles', 1),
    (9, 'export_data', 1),
    (10, 'import_data', 1);
    """
    sql_select = "SELECT * FROM functions_dict;"
    with Session(engine) as session:
        session.exec(text(sql_insert))
        session.commit()
        roles = session.exec(text(sql_select)).fetchall()
    print(f"{roles=}")


def assign_functions_roles():
    print()
    print("Fill role_functions data...")
    sql_insert = """
    INSERT INTO role_functions  (role_id, function_code_id) VALUES
    (1, 1);
    """
    sql_select = "SELECT * FROM role_functions;"
    with Session(engine) as session:
        session.exec(text(sql_insert))
        session.commit()
        roles = session.exec(text(sql_select)).fetchall()
    print(f"{roles=}")


def main():
    generate_timezone_dict()
    generate_test_company_data()
    generate_settings_dict()
    generate_settings()
    generate_roles_dict()
    generate_functions_dict()
    assign_functions_roles()


if __name__ == "__main__":
    main()
