import sys
from urllib.parse import urlparse
import whois


def clean_domain_input(user_input: str) -> str:
    """
    Очищает ввод пользователя, удаляя протоколы (http/https),
    лишние пробелы и пути, возвращая чистый домен.
    """
    # Удаляем случайные пробелы по краям
    cleaned = user_input.strip().lower()

    # Если ввели полноценный URL (например, https://example.com), извлекаем хост
    if cleaned.startswith(('http://', 'https://')):
        parsed = urlparse(cleaned)
        cleaned = parsed.netloc

    # Удаляем 'www.', если оно присутствует
    if cleaned.startswith('www.'):
        cleaned = cleaned[4:]

    # На случай, если ввели "://example.com", убираем слеши
    cleaned = cleaned.split('/')[0]

    return cleaned


def fetch_whois_data(domain: str):
    """
    Запрашивает сырые данные WHOIS для указанного домена.
    Возвращает объект WHOIS или генерирует ошибку.
    """
    cleaned_domain = clean_domain_input(domain)

    if not cleaned_domain:
        raise ValueError("Передано пустое или некорректное имя домена.")

    try:
        # Библиотека сама выберет нужный WHOIS-сервер на основе TLD (.com, .ru и т.д.)
        raw_data = whois.whois(cleaned_domain)
        return raw_data
    except Exception as e:
        raise RuntimeError(f"Ошибка при запросе к WHOIS для '{cleaned_domain}': {e}")


# Блок для автономного тестирования модуля
if __name__ == "__main__":
    print("--- Автономный тест модуля api_client.py ---")

    # Проверяем, передан ли домен аргументом командной строки
    if len(sys.argv) > 1:
        test_domain = sys.argv[1]
    else:
        # Если аргумента нет, запрашиваем через инпут
        test_domain = input("Введите домен для проверки (например, google.com): ")

    print(f"\n[1/2] Очистка ввода...")
    ready_domain = clean_domain_input(test_domain)
    print(f"Результат очистки: '{ready_domain}'")

    print(f"\n[2/2] Отправка запроса на сервер WHOIS...")
    try:
        result = fetch_whois_data(ready_domain)

        print("\n[УСПЕХ] Данные успешно получены!")
        print("-" * 40)
        # Выводим первые 15 строк сырого ответа, чтобы не перегружать консоль
        raw_text_lines = str(result).split('\n')
        for line in raw_text_lines[:15]:
            print(line)
        if len(raw_text_lines) > 15:
            print("... и еще часть данных скрыта (модуль работает исправно) ...")
        print("-" * 40)

    except Exception as error:
        print(f"\n[ОШИБКА] Не удалось выполнить тест.")
        print(f"Детали: {error}")
