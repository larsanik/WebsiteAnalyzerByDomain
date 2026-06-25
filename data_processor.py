from datetime import datetime
import json  # Используется исключительно для красивого вывода словаря в тесте
# Импортируем api_client для проведения автономного тестирования в конце файла
import api_client


def _normalize_date(date_field) -> str:
    """
    Вспомогательная функция для приведения дат к единому строковому формату.
    Учитывает, что WHOIS может вернуть объект datetime, список дат или строку.
    """
    if not date_field:
        return "Нет данных"

    # Если сервер вернул список дат (историю обновлений), берем самый первый/актуальный элемент
    if isinstance(date_field, list):
        date_field = date_field[0]

    if isinstance(date_field, datetime):
        return date_field.strftime("%Y-%m-%d %H:%M:%S")

    return str(date_field).strip()


def _normalize_list_or_str(field) -> str:
    """
    Вспомогательная функция для текстовых полей и списков (DNS-серверы, статусы).
    Объединяет списки в строку через запятую или возвращает очищенную строку.
    """
    if not field:
        return "Нет данных"

    if isinstance(field, list):
        # Удаляем дубликаты, сохраняя порядок, очищаем от пробелов и склеиваем
        seen = set()
        unique_items = [str(item).strip() for item in field if
                        not (str(item).strip() in seen or seen.add(str(item).strip()))]
        return ", ".join(unique_items)

    return str(field).strip()


def process_whois_data(raw_data) -> dict:
    """
    Принимает сырой объект WHOIS от api_client и извлекает из него
    9 строго определенных полей, гарантируя строковый тип данных на выходе.
    """
    if not raw_data:
        raise ValueError("Получены пустые данные для обработки.")

    # Создаем структурированный словарь на основе вашего ТЗ
    processed_data = {
        "Доменное имя": _normalize_list_or_str(raw_data.get("domain_name")),
        "Владелец или организация": _normalize_list_or_str(raw_data.get("org") or raw_data.get("name")),
        "Регистратор": _normalize_list_or_str(raw_data.get("registrar")),
        "Дата регистрации": _normalize_date(raw_data.get("creation_date")),
        "Дата истечения": _normalize_date(raw_data.get("expiration_date")),
        "Дата последнего обновления": _normalize_date(raw_data.get("updated_date")),
        "Серверы имён": _normalize_list_or_str(raw_data.get("name_servers")),
        "Статус домена": _normalize_list_or_str(raw_data.get("status")),
        "Страна регистранта": _normalize_list_or_str(raw_data.get("country"))
    }

    return processed_data


# Блок для автономного тестирования модуля
if __name__ == "__main__":
    print("--- Автономный тест модуля data_processor.py ---")
    target_domain = "yandex.ru"

    print(f"\n[1/3] Запрашиваем сырые данные через api_client для {target_domain}...")
    try:
        raw_info = api_client.fetch_whois_data(target_domain)
        print("[УСПЕХ] Сырые данные получены.")

        print(f"\n[2/3] Обрабатываем и нормализуем данные в data_processor...")
        structured_data = process_whois_data(raw_info)
        print("[УСПЕХ] Данные успешно очищены и структурированы.")

        print(f"\n[3/3] Результат обработки (итоговый словарь):")
        print("-" * 50)
        # Выводим словарь в красивом JSON-формате с отступами для читаемости
        print(json.dumps(structured_data, ensure_ascii=False, indent=4))
        print("-" * 50)

    except Exception as error:
        print(f"\n[ОШИБКА] Не удалось выполнить совместный тест модулей.")
        print(f"Детали: {error}")
