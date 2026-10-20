import argparse
import os


def parse_arguments():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализатор пакетов: минимальный прототип."
    )

    parser.add_argument(
        "--package",
        type=str,
        help="Имя пакета"
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="URL репозитория или путь"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["test", "prod"],
        help="Режим (test/prod)"
    )
    parser.add_argument(
        "--version",
        type=str,
        help="Версия пакета"
    )
    parser.add_argument(
        "--filter",
        type=str,
        help="Фильтр пакетов"
    )

    return parser.parse_args()


def read_file_safely(file_path):
    """Безопасно читает файл и возвращает список строк."""
    if not os.path.exists(file_path):
        print(f"Ошибка: файл не найден: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except Exception as error:
        print(f"Ошибка при чтении файла: {error}")
        return []


def parse_cargo_dependencies(file_path):
    """Читает Cargo.toml и возвращает список зависимостей."""
    lines = read_file_safely(file_path)
    if not lines:
        return []

    dependencies = []
    in_dependencies_section = False

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("[") and line.endswith("]"):
            in_dependencies_section = (line == "[dependencies]")
            continue

        if in_dependencies_section:
            package_name = line.split("=")[0].strip()
            if package_name:
                dependencies.append(package_name)

    return dependencies


def main():
    """Точка входа. Выводит параметры и зависимости."""
    args = parse_arguments()

    print("=== Параметры запуска ===")
    print(f"package = {args.package}")
    print(f"repo    = {args.repo}")
    print(f"mode    = {args.mode}")
    print(f"version = {args.version}")
    print(f"filter  = {args.filter}")
    print("=========================\n")

    if args.repo:
        print(f"Анализ зависимостей: {args.repo}")
        deps = parse_cargo_dependencies(args.repo)

        if deps:
            print("Прямые зависимости:")
            for dep in deps:
                print(f" - {dep}")
        else:
            print("Зависимости не найдены.")
    else:
        print("Файл репозитория не указан (флаг --repo).")


if __name__ == "__main__":
    main()