from faker import Faker
from faker.providers import BaseProvider


class RussianBusinessProvider(BaseProvider):
    """Расширенный провайдер для российского бизнеса"""

    _boolean = True
    # Списки данных для генерации
    COMPANY_TYPES = ["ООО", "АО", "ЗАО", "ИП", "НКО", "ГУП", "МУП"]
    TAX_SYSTEMS = ["ОСН", "УСН", "ЕНВД", "ЕСХН", "ПСН"]
    COMPANY_SUFFIXES = ["Групп", "Холдинг", "Инвест", "Трейд", "Сервис", "Технологии"]

    # Словарь популярных ОКВЭД с описаниями
    OKVED_CODES = {
        "62.01": "Разработка компьютерного программного обеспечения",
        "47.11": "Торговля розничная в неспециализированных магазинах",
        "49.41": "Деятельность автомобильного грузового транспорта",
        "68.20": "Аренда и управление собственным или арендованным недвижимым имуществом",
        "43.21": "Производство электромонтажных работ",
    }

    def russian_company_type(self):
        """Тип юридического лица"""
        return self.random_element(self.COMPANY_TYPES)

    def russian_company_name(self, company_type=None):
        """Генерация названия компании"""
        if company_type is None:
            company_type = self.russian_company_type()

        # База слов для названий
        words = [
            "Север",
            "Юг",
            "Восток",
            "Запад",
            "Техно",
            "Бизнес",
            "Профи",
            "Стандарт",
            "Элит",
            "Глобал",
            "Металл",
            "Строй",
            "Нефть",
            "Газ",
        ]

        name_parts = [
            self.random_element(words),
            self.random_element(words),
            self.random_element(self.COMPANY_SUFFIXES),
        ]

        # Убираем возможные дубликаты
        unique_parts = list(dict.fromkeys(name_parts))
        company_name = " ".join(unique_parts)

        return f"{company_type} «{company_name}»"

    def russian_okved(self, with_description=False):
        """Генерация кода ОКВЭД"""
        if with_description:
            # Возвращаем случайный ОКВЭД с описанием
            code, description = self.random_element(list(self.OKVED_CODES.items()))
            return {"code": code, "description": description}
        else:
            # Генерация случайного кода
            main = str(self.random_int(10, 99))
            sub = str(self.random_int(10, 99)) if self._boolean else ""
            return f"{main}.{sub}" if sub else main

    @property
    def boolean(self):
        return self._boolean

    @boolean.setter
    def boolean(self, value: bool):
        self._boolean = value

    def russian_tax_system(self):
        """Система налогообложения"""
        return self.random_element(self.TAX_SYSTEMS)

    def russian_inn(self, for_individual=False):
        """Генерация ИНН"""
        if for_individual:
            # ИНН для физического лица (12 цифр)
            inn = "".join([str(self.random_int(0, 9)) for _ in range(12)])
        else:
            # ИНН для юридического лица (10 цифр)
            inn = "".join([str(self.random_int(0, 9)) for _ in range(10)])
        return inn

    def russian_ogrn(self):
        """Генерация ОГРН"""
        # Пример генерации для юрлица (13 цифр):
        ogrn = "102" + "".join([str(self.random_int(0, 9)) for _ in range(10)])

        # Пример генерации для ИП (15 цифр):
        # ogrn_individual = "301" + "".join(
        # [str(self.random_int(0, 9)) for _ in range(15)]
        # )
        return ogrn

    def russian_kpp(self):
        """Генерация КПП"""
        return "".join([str(self.random_int(0, 9)) for _ in range(9)])

    def russian_bank_account(self):
        """Генерация банковского счета"""
        return "".join([str(self.random_int(0, 9)) for _ in range(20)])

    def russian_business_address(self):
        """Юридический адрес"""
        cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
        streets = [
            "ул. Ленина",
            "пр. Мира",
            "ул. Советская",
            "ул. Центральная",
            "пр. Победы",
        ]

        return f"{self.random_element(cities)}, {self.random_element(streets)}, {self.random_int(1, 100)}"


def test_generate_company():
    # Регистрация провайдера
    fake = Faker("ru_RU")
    fake.add_provider(RussianBusinessProvider)

    # Демонстрация работы
    print("=== ГЕНЕРАЦИЯ ДАННЫХ РОССИЙСКОГО БИЗНЕСА ===")
    print()

    # Базовая информация
    company_type = fake.russian_company_type()
    company_name = fake.russian_company_name(company_type)
    print(f"Название компании: {company_name}")
    print(f"Юридический адрес: {fake.russian_business_address()}")
    print()

    # Реквизиты
    inn = fake.russian_inn()
    kpp = fake.russian_kpp()
    ogrn = fake.russian_ogrn()
    print("Реквизиты:")
    print(f"ИНН: {inn}")
    print(f"КПП: {kpp}")
    print(f"ОКВЭД: {fake.russian_okved()}")
    print(f"ОГРН: {ogrn}")
    print(f"Система налогообложения: {fake.russian_tax_system()}")
    print()

    # Банковские реквизиты
    bic = fake.random_int(100000000, 999999999)
    print("Банковские реквизиты:")
    print(f"Расчетный счет: {fake.russian_bank_account()}")
    print(f"Банк: {fake.company()}")
    print(f"БИК: {bic}")
    print()

    # Детальная информация по ОКВЭД
    okved_details = fake.russian_okved(with_description=True)
    print(
        f"Детализация ОКВЭД: {okved_details['code']} - {okved_details['description']}"
    )
