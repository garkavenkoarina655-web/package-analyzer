import argparse
import os


def parse_arguments():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализатор пакетов."
    )
    parser.add_argument("--package", type=str, help="Имя пакета")
    parser.add_argument("--repo", type=str, help="Путь к файлу")
    parser.add_argument(
        "--mode", type=str, choices=["test", "prod"], help="Режим"
    )
    parser.add_argument("--version", type=str, help="Версия")
    parser.add_argument("--filter", type=str, help="Фильтр")
    return parser.parse_args()


def read_file_safely(file_path):
    """Безопасно читает файл."""
    if not os.path.exists(file_path):
        print(f"Ошибка: файл не найден: {file_path}")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()
    except Exception as error:
        print(f"Ошибка чтения: {error}")
        return []


def parse_cargo_lock(file_path):
    """Парсит Cargo.lock и строит граф зависимостей."""
    graph = {}
    lines = read_file_safely(file_path)
    current_package = None
    in_deps = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("[[package]]"):
            current_package = None
            in_deps = False
        elif line.startswith("name = ") and current_package is None:
            current_package = line.split("=")[1].strip().strip('"')
            graph[current_package] = []
        elif line.startswith("dependencies = ["):
            in_deps = True
        elif line.startswith("]") and in_deps:
            in_deps = False
        elif in_deps and current_package:
            dep_name = line.split(",")[0].strip().strip('"')
            if dep_name:
                graph[current_package].append(dep_name)
    return graph


def bfs_recursive(graph, queue, visited, ignore_filter, result):
    """Рекурсивный BFS для поиска всех зависимостей."""
    if not queue:
        return result

    current = queue.pop(0)

    if ignore_filter and ignore_filter in current:
        return bfs_recursive(graph, queue, visited, ignore_filter, result)

    if current not in result:
        result.append(current)

    for neighbor in graph.get(current, []):
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)

    return bfs_recursive(graph, queue, visited, ignore_filter, result)


def process_cargo(repo_path, package, ignore_filter):
    """Запускает анализ Cargo.lock."""
    print(f"Анализ файла: {repo_path}")
    graph = parse_cargo_lock(repo_path)

    if package not in graph:
        print(f"Пакет '{package}' не найден.")
        return

    print(f"Транзитивные зависимости {package}:")
    queue = [package]
    visited = set([package])
    result = []

    bfs_recursive(graph, queue, visited, ignore_filter, result)

    for dep in result:
        print(f" - {dep}")


def main():
    """Точка входа."""
    args = parse_arguments()

    print(f"Пакет: {args.package}")
    print(f"Файл:  {args.repo}")
    print(f"Фильтр: {args.filter}")
    print("-" * 20)

    if not args.repo:
        print("Укажите файл через --repo")
        return

    if args.package:
        process_cargo(args.repo, args.package, args.filter)
    else:
        print("Укажите имя пакета через --package")


if __name__ == "__main__":
    main()