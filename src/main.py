import argparse
import os

def parse_arguments():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализатор пакетов: минимальный прототип."
    )

    parser.add_argument("--package", type=str, help="Имя пакета")
    parser.add_argument("--repo", type=str, help="URL репозитория или путь")
    parser.add_argument("--mode", type=str, choices=["test", "prod"], help="Режим (test/prod)")
    parser.add_argument("--version", type=str, help="Версия пакета")
    parser.add_argument("--filter", type=str, help="Фильтр пакетов")

    return parser.parse_args()


def parse_cargo_dependencies(file_path):
    """Читает Cargo.toml и возвращает список прямых зависимостей."""
    if not os.path.exists(file_path):
        print(f"Ошибка: файл не найден по пути {file_path}")
        return []

    dependencies = []
    in_dependencies_section = False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # Пропускаем пустые строки и комментарии
                if not line or line.startswith("#"):
                    continue

                # Проверяем, не начался ли раздел зависимостей
                if line.startswith("[") and line.endswith("]"):
                    if line == "[dependencies]":
                        in_dependencies_section = True
                    else:
                        in_dependencies_section = False
                    continue

                # Если мы внутри раздела зависимостей, извлекаем имя пакета
                if in_dependencies_section:
                    # Берем всё до знака '='
                    package_name = line.split("=")[0].strip()
                    if package_name:
                        dependencies.append(package_name)

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

    return dependencies


def main():
    """Точка входа. Выводит параметры и прямые зависимости."""
    args = parse_arguments()

    print("=== Параметры запуска ===")
    print(f"package = {args.package}")
    print(f"repo    = {args.repo}")
    print(f"mode    = {args.mode}")
    print(f"version = {args.version}")
    print(f"filter  = {args.filter}")
    print("=========================\n")

    # Если пользователь передал путь к файлу в --repo
    if args.repo:
        print(f"Анализ зависимостей из файла: {args.repo}")
        deps = parse_cargo_dependencies(args.repo)

        if deps:
            print("Прямые зависимости:")
            for dep in deps:
                print(f" - {dep}")
        else:
            print("Зависимости не найдены или файл пуст.")
    else:
        print("Файл репозитория не указан (флаг --repo). Анализ не выполнен.")

if __name__ == "__main__":
    main()