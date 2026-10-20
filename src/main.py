import argparse


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


def main():
    """Точка входа. Выводит параметры."""
    args = parse_arguments()

    print("=== Параметры запуска ===")
    print(f"package = {args.package}")
    print(f"repo    = {args.repo}")
    print(f"mode    = {args.mode}")
    print(f"version = {args.version}")
    print(f"filter  = {args.filter}")
    print("=========================")


if __name__ == "__main__":
    main()