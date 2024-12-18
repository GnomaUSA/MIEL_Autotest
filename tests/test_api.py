import os.path
import pytest
import json
from pprint import pprint

from miel_api import MielAPIManager
from setting import valid_email, valid_password

mam = MielAPIManager()

@pytest.fixture
def access_token():
    """
    Фикстура для получения токена авторизации.
    Использует валидные данные из setting.
    """
    # Используем уже созданный экземпляр mam
    _, token_response = mam.post_api_token(valid_email, valid_password)

    # Возвращаем токен из ответа
    return token_response['access_token']
def test_post_api_token_for_valid_user(email=valid_email, password=valid_password):

    # Тест на проверку получения токена.
    status, result = mam.post_api_token(email, password)

    # Проверяем статус ответа
    assert status == 200, f"Ожидался статус 200, а получен {status}"

    # Проверяем, что в ответе есть ключ 'access_token'
    assert 'access_token' in result, "Ответ не содержит ключа 'access_token'"

    # Проверяем, что токен не пустой
    assert result['access_token'], "Поле 'access_token' пустое"

    # Вывод токена для отладки (опционально)
    pprint(f"Полученный токен: {result['access_token']}")

def test_get_manager(access_token):

    # Тест на получение информации о менеджере
    status, result = mam.get_manager(access_token)

    print("\nКоличество доступных кандидатов:", len(result))
    # Преобразуем результат в читаемый формат
    formatted_result = json.dumps(result, indent=4, ensure_ascii=False)
    print(formatted_result)


    # Проверяем, что статус ответа 200
    assert status == 200, f"Ожидался статус 200, а получен {status}"

    # Проверяем, что ответ содержит основные ключи
    assert 'full_name' in result, "Ответ не содержит ключ 'full_name'"
    assert 'email' in result, "Ответ не содержит ключ 'email'"
    assert 'candidates' in result, "Ответ не содержит ключ 'candidates'"
    assert 'office' in result, "Ответ не содержит ключ 'office'"

    # Проверяем типы данных
    assert isinstance(result['full_name'], str), "Поле 'full_name' должно быть строкой"
    assert len(result['full_name'].strip()) > 0, "Поле 'full_name' не должно быть пустым"
    assert isinstance(result['email'], str), "Поле 'email' должно быть строкой"
    assert len(result['email'].strip()) > 0, "Поле 'email' не должно быть пустым"
    assert isinstance(result['candidates'], list), "Поле 'candidates' должно быть списком"
    assert isinstance(result['office'], dict), "Поле 'office' должно быть словарём"

    # Проверяем, что список кандидатов не пустой
    assert len(result['candidates']) > 0, "Список кандидатов пустой"

    # Проверяем структуру и содержимое кандидатов
    for candidate in result['candidates']:
        assert 'candidate_id' in candidate, "Кандидат не содержит ключ 'candidate_id'"
        assert 'is_viewed' in candidate, "Кандидат не содержит ключ 'is_viewed'"
        assert 'is_favorite' in candidate, "Кандидат не содержит ключ 'is_favorite'"
        assert isinstance(candidate['candidate_id'], int), "Поле 'candidate_id' должно быть целым числом"
        assert isinstance(candidate['is_viewed'], bool), "Поле 'is_viewed' должно быть булевым"
        assert isinstance(candidate['is_favorite'], bool), "Поле 'is_favorite' должно быть булевым"

    # Проверяем структуру офиса
    office = result['office']
    assert 'location' in office, "Ответ не содержит ключ 'location' в 'office'"
    assert 'name' in office, "Ответ не содержит ключ 'name' в 'office'"
    assert 'id' in office, "Ответ не содержит ключ 'id' в 'office'"
    assert isinstance(office['location'], str), "Поле 'location' должно быть строкой"
    assert isinstance(office['name'], str), "Поле 'name' должно быть строкой"
    assert isinstance(office['id'], int), "Поле 'id' должно быть целым числом"

def test_get_candidates_of_manager(access_token):

    # Тест на получение списка кандидатов менеджера с проверкой формата JSON и структуры ответа.
    status, result = mam.get_candidates_of_manager(access_token)

    # Проверяем статус ответа
    assert status == 200, f"Ожидался статус 200, а получен {status}"

    # Проверяем, что результат можно преобразовать в JSON
    try:
        json.dumps(result)
    except (TypeError, ValueError):
        assert False, "Ответ не соответствует формату JSON"

    # Проверяем, что результат — список
    assert isinstance(result, list), "Ответ должен быть списком"

    # Проверяем, что список не пустой
    assert len(result) > 0, "Список кандидатов пустой"

    print("\nКоличество кандидатов:", len(result))
    # Выводим результат в удобном формате для отладки
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # Проверяем, что каждый элемент списка имеет нужные ключи и правильные типы данных
    required_keys = {
        "photo": str,
        "full_name": str,
        "location": str,
        "phone": str,
        "clients": int,
        "objects": int,
        "created_at": str,
        "updated_at": str,
        "id": int,
        "email": str,
        "resume": str,
        "is_hired": bool
    }

    for candidate in result:
        # Проверяем, что у кандидата есть все обязательные ключи
        for key, expected_type in required_keys.items():
            assert key in candidate, f"Кандидат не содержит ключ '{key}'"
            assert isinstance(candidate[key], expected_type), (
                f"Ключ '{key}' имеет некорректный тип: ожидался {expected_type}, "
                f"а получен {type(candidate[key])}"
            )

    # Дополнительно проверяем корректность формата временных меток
    for candidate in result:
        try:
            from datetime import datetime
            datetime.fromisoformat(candidate['created_at'])
            datetime.fromisoformat(candidate['updated_at'])
        except ValueError:
            assert False, f"Временные метки в кандидате имеют некорректный формат: {candidate}"

def test_get_available_candidates(access_token):
    # Тест на получение списка всех кандидатов доступных к найму с проверкой формата JSON
    # и структуры ответа.
    status, result = mam.get_candidates_of_manager(access_token)

    # Проверяем статус ответа
    assert status == 200, f"Ожидался статус 200, а получен {status}"

    # Проверяем, что результат можно преобразовать в JSON
    try:
        json.dumps(result)
    except (TypeError, ValueError):
        assert False, "Ответ не соответствует формату JSON"

    # Проверяем, что результат — список
    assert isinstance(result, list), "Ответ должен быть списком"

    # Проверяем, что список не пустой
    assert len(result) > 0, "Список кандидатов пустой"

    print("\nКоличество доступных кандидатов:", len(result))
    # Выводим результат в удобном формате для отладки
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # Проверяем, что каждый элемент списка имеет нужные ключи и правильные типы данных
    required_keys = {
        "photo": str,
        "full_name": str,
        "location": str,
        "phone": str,
        "clients": int,
        "objects": int,
        "created_at": str,
        "updated_at": str,
        "id": int,
        "email": str,
        "resume": str,
        "is_hired": bool
    }

    for candidate in result:
        # Проверяем, что у кандидата есть все обязательные ключи
        for key, expected_type in required_keys.items():
            assert key in candidate, f"Кандидат не содержит ключ '{key}'"
            assert isinstance(candidate[key], expected_type), (
                f"Ключ '{key}' имеет некорректный тип: ожидался {expected_type}, "
                f"а получен {type(candidate[key])}"
            )

    # Дополнительно проверяем корректность формата временных меток
    for candidate in result:
        try:
            from datetime import datetime
            datetime.fromisoformat(candidate['created_at'])
            datetime.fromisoformat(candidate['updated_at'])
        except ValueError:
            assert False, f"Временные метки в кандидате имеют некорректный формат: {candidate}"

def test_get_candidates_with_filter(access_token):
    """
    Тест на проверку метода GET с фильтрацией кандидатов по 'is_hired'.
    """

    # Фильтр: is_hired=True
    status, result = mam.get_candidates(access_token, is_hired=True)

    # Проверка статуса и результата
    assert status == 200, "Ожидался статус 200"
    assert isinstance(result, list), "Ответ должен быть списком"

    print("\nФильтр: is_hired=True")
    print(f"Количество кандидатов: {len(result)}")

    # Проверка, что все кандидаты соответствуют фильтру
    for candidate in result:
        assert 'is_hired' in candidate, "Ответ не содержит ключ 'is_hired'"
        assert candidate['is_hired'] is True, "Кандидат не соответствует фильтру 'is_hired=True'"

    pprint(result)  # Форматированный вывод

    # Фильтр: is_hired=False
    status, result = mam.get_candidates(access_token, is_hired=False)

    # Проверка статуса и результата
    assert status == 200, "Ожидался статус 200"
    assert isinstance(result, list), "Ответ должен быть списком"

    print("\nФильтр: is_hired=False")
    print(f"Количество кандидатов: {len(result)}")

    # Проверка, что все кандидаты соответствуют фильтру
    for candidate in result:
        assert 'is_hired' in candidate, "Ответ не содержит ключ 'is_hired'"

        # Отладочный вывод для каждого кандидата
        print(f"Кандидат ID: {candidate['id']}, is_hired: {candidate['is_hired']}")

        # Проверка соответствия значению фильтра
        assert candidate['is_hired'] is True, "Кандидат не соответствует фильтру 'is_hired=True'"

        # Форматированный вывод всего результата для отладки
    from pprint import pprint
    pprint(result)