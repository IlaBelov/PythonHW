import requests


class YougileClient:
    BASE_URL = "https://ru.yougile.com/api-v2"

    def __init__(self, api_key=""):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def create_project(self, title):
        resp = requests.post(
            f"{self.BASE_URL}/projects",
            json={"title": title},
            headers=self.headers
        )
        return resp

    def get_project(self, project_id):
        resp = requests.get(
            f"{self.BASE_URL}/projects/{project_id}",
            headers=self.headers
        )
        return resp

    def update_project(self, project_id, title):
        resp = requests.put(
            f"{self.BASE_URL}/projects/{project_id}",
            json={"title": title},
            headers=self.headers
        )
        return resp


# ПОЗИТИВНЫЕ ТЕСТЫ
def test_create_project_positive():
    client = YougileClient()
    resp = client.create_project("Тестовый проект")

    assert resp.status_code in [200, 201], f"Status code: {resp.status_code}"

    data = resp.json()
    assert "id" in data
    return data["id"]


def test_get_project_positive():
    client = YougileClient()

    create_resp = client.create_project("Проект для получения")
    assert create_resp.status_code in [200, 201]

    project_id = create_resp.json()["id"]

    resp = client.get_project(project_id)
    assert resp.status_code == 200, f"Status code: {resp.status_code}"

    data = resp.json()
    assert data["id"] == project_id
    assert data["title"] == "Проект для получения"


def test_update_project_positive():
    client = YougileClient()

    create_resp = client.create_project("Старое название")
    assert create_resp.status_code in [200, 201]

    project_id = create_resp.json()["id"]

    resp = client.update_project(project_id, "Новое название")
    assert resp.status_code == 200, f"Status code: {resp.status_code}"


# Негативные тесты
def test_create_project_negative():
    client = YougileClient()
    resp = client.create_project("")

    assert resp.status_code in [400, 422], f"Status code: {resp.status_code}"


def test_get_project_negative():
    client = YougileClient()
    resp = client.get_project("non-existent-123")

    assert resp.status_code == 404, f"Status code: {resp.status_code}"


def test_update_project_negative():
    client = YougileClient()
    resp = client.update_project("non-existent-456", "Новое название")

    assert resp.status_code == 404, f"Status code: {resp.status_code}"


if __name__ == "__main__":
    print("=== Запуск позитивных тестов ===")

    print("1. Тест создания проекта...")
    project_id = test_create_project_positive()
    print(f"   ✓ Создан проект с ID: {project_id}")

    print("2. Тест получения проекта...")
    test_get_project_positive()
    print("   ✓ Проект успешно получен")

    print("3. Тест обновления проекта...")
    test_update_project_positive()
    print("   ✓ Проект успешно обновлен")

    print("\n=== Запуск негативных тестов ===")

    print("1. Тест создания без названия...")
    test_create_project_negative()
    print("   ✓ Ошибка валидации получена")

    print("2. Тест получения несуществующего проекта...")
    test_get_project_negative()
    print("   ✓ Ошибка 404 получена")

    print("3. Тест обновления несуществующего проекта...")
    test_update_project_negative()
    print("   ✓ Ошибка 404 получена")

    print("\n✓ Все тесты успешно пройдены!")
