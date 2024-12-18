import requests

class MielAPIManager:
    def __init__(self):
        self.base_url = "https://backend-y9b6.onrender.com/"


    def post_api_token(self, email : str, password : str):
        """
        Метод делает POST-запрос к API сервера и возвращает статус запроса и результат в формате JSON
        с уникальным ключом пользователя, найденного по указанным email и паролю.
        """
        data = {
            'email': email,
            'password': password
        }

        res = requests.post(self.base_url + 'auth/login/', data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except ValueError:
            result = res.text

        # print(result)
        return status, result

    def get_manager(self, access_token: str):
        """
        Метод делает GET-запрос к API для получения информации о менеджере.
        Токен используется для авторизации.
        """
        # Формируем заголовки с токеном
        headers = {'Authorization': f"Bearer {access_token}"}

        # Отправляем запрос
        res = requests.get(self.base_url + 'manager/', headers=headers)

        # Извлекаем статус и результат
        status = res.status_code  # Исправлено: res.status.code -> res.status_code
        try:
            result = res.json()  # Преобразуем ответ в JSON, если возможно
        except ValueError:
            result = res.text  # Если не JSON, возвращаем текст

        # Выводим результат для отладки
        # print(result)
        return status, result

    def get_candidates_of_manager(self, access_token: str):
        """
               Метод делает GET-запрос к API для получения информации о всех кандидатах.
               Токен используется для авторизации.
               """
        # Формируем заголовки с токеном
        headers = {'Authorization': f"Bearer {access_token}"}  # Добавлен пробел после "Bearer"

        # Отправляем запрос
        res = requests.get(self.base_url + 'manager/get_candidates/', headers=headers)

        # Извлекаем статус и результат
        status = res.status_code
        try:
            result = res.json()  # Преобразуем ответ в JSON, если возможно
        except ValueError:
            result = res.text  # Если не JSON, возвращаем текст

        # Выводим результат для отладки
        # print(result)
        return status, result

    def get_available_candidates(self, access_token: str):
        """
               Метод делает GET-запрос к API для получения информации о кандидатах,
               доступных менеджеру.
               Токен используется для авторизации.
               """
        # Формируем заголовки с токеном
        headers = {'Authorization': f"Bearer {access_token}"}  # Добавлен пробел после "Bearer"

        # Отправляем запрос
        res = requests.get(self.base_url + 'manager/get_available_candidates/', headers=headers)

        # Извлекаем статус и результат
        status = res.status_code
        try:
            result = res.json()  # Преобразуем ответ в JSON, если возможно
        except ValueError:
            result = res.text  # Если не JSON, возвращаем текст

        # Выводим результат для отладки
        # print(result)
        return status, result

    def get_candidate_by_id(self, access_token : str, candidate_id : int):
        """
               Метод делает GET-запрос к API для получения информации о кандидатах,
               используя id кандидата.
               Токен используется для авторизации.
               """
        # Формируем заголовки с токеном
        headers = {'Authorization': f"Bearer {access_token}"}
        params = {'candidate_id' : candidate_id}

        # Отправляем запрос
        res = requests.get(self.base_url + 'manager/get_candidate_by_id/', headers=headers, params=params)

        # Извлекаем статус и результат
        status = res.status_code
        try:
            result = res.json()  # Преобразуем ответ в JSON, если возможно
        except ValueError:
            result = res.text  # Если не JSON, возвращаем текст

        # Выводим результат для отладки
        # print(result)
        return status, result

    def get_candidates(self, auth_token: str, is_hired: bool = None):
        """
        Получение списка кандидатов с фильтрацией по полю 'is_hired'.
        """
        headers = {'Authorization': f"Bearer {auth_token}"}
        params = {'is_hired': is_hired} if is_hired is not None else {}

        response = requests.get(self.base_url + 'manager/get_available_candidates/', headers=headers, params=params)
        return response.status_code, response.json()
