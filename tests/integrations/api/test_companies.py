from fastapi.testclient import TestClient

from app.core.database.models import Companies
from app.main import app

ENDPOINT = "api/v1/companies/"


def test_get_company():
    company_id = "1"
    with TestClient(app) as client:
        response = client.get(ENDPOINT + company_id)
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_list_company():
    with TestClient(app) as client:
        response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert response.json() != []
    response_json = response.json()
    assert isinstance(response_json, list)
    assert isinstance(response_json[0], dict)
    print(f"{response_json=}")


def test_create_delete_company():
    company = Companies(
        property_id=1,
        name="Test Company",
        kpp="562596571",
        bic="466072470",
        inn="3375642255",
        ogrn="1021712356460",
    )
    with TestClient(app) as client:
        response = client.post(ENDPOINT, data=company.model_dump_json())
        assert response.status_code == 200
        response_json = response.json()
        assert isinstance(response_json, dict)
        print()
        print(f"{response_json=}")

    company_id = response_json["id"]
    with TestClient(app) as client:
        response = client.delete(ENDPOINT + str(company_id))
    assert response.status_code == 201
    response_json = response.json()
    print(f"{response_json=}")
