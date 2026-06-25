import sys
# Импортируем наши собственные модули
import api_client
import data_processor
import report


def run_analyzer():
    """
    Основная логика запуска анализатора доменов.
    """
    print("=" * 60)
    print(" CLI-АНАЛИЗАТОР КОНКУРЕНТОВ ПО ДОМЕНУ ".center(60, " "))
    print("=" * 60)

    # Запрашиваем ввод у пользователя
    user_input = input("Введите адрес сайта для анализа (или 'exit' для выхода): ")

    # Проверяем команду на выход
    if user_input.strip().lower() in ('exit', 'quit', 'выход'):
        print("\nЗавершение работы программы. Всего доброго!")
        sys.exit(0)

    print("\n[Процесс] Начинаем сбор и обработку информации...")

    try:
        # Шаг 1: Очищаем ввод и запрашиваем сырые данные через api_client
        # (Очистку вызываем превентивно, чтобы вывести пользователю финальный домен)
        cleaned_domain = api_client.clean_domain_input(user_input)
        if not cleaned_domain:
            raise ValueError("Введена пустая строка или некорректные символы.")

        print(f"[1/3] Подключение к серверу WHOIS для домена '{cleaned_domain}'...")
        raw_data = api_client.fetch_whois_data(cleaned_domain)

        # Шаг 2: Передаем сырые данные на фильтрацию и нормализацию в data_processor
        print("[2/3] Извлечение и структурирование данных...")
        structured_data = data_processor.process_whois_data(raw_data)

        # Корректируем поле домена на тот случай, если WHOIS вернул его пустым
        if structured_data.get("Доменное имя") == "Нет данных":
            structured_data["Доменное имя"] = cleaned_domain

        # Шаг 3: Передаем готовый словарь в report для красивого вывода в CLI
        print("[3/3] Формирование финального отчета...")
        report.generate_report(structured_data)

    except ValueError as val_err:
        print(f"\n[ОШИБКА ВВОДА] {val_err}")
    except RuntimeError as run_err:
        print(f"\n[ОШИБКА СЕТИ / WHOIS] {run_err}")
    except Exception as e:
        print(f"\n[НЕПРЕДВИДЕННАЯ ОШИБКА] Что-то пошло не так: {e}")


if __name__ == "__main__":
    # Запускаем программу в бесконечном цикле, пока пользователь не решит выйти
    while True:
        try:
            run_analyzer()
            print("-" * 60)
            # Небольшая пауза перед следующим вводом
            input("Нажмите Enter, чтобы продолжить...")
            print("\n" * 2)  # Отступаем место для чистоты экрана
        except KeyboardInterrupt:
            # Корректно обрабатываем нажатие Ctrl+C
            print("\n\nПрограмма принудительно завершена пользователем.")
            sys.exit(0)
