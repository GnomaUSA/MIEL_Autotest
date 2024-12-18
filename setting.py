import os
# используется для работы с переменными окружения.

from dotenv import load_dotenv
# позволяет загружать переменные окружения из файла .env.

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')