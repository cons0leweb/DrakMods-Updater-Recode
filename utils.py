import os
import hashlib
import git
import shutil
import json
from rich.console import Console

console = Console()

def calculate_file_hash(file_path):
    """Вычисляет MD5 хеш файла."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        return None

def get_files_hashes(dir_path):
    """Возвращает словарь с хешами всех файлов в директории."""
    file_hashes = {}
    for root, _, files in os.walk(dir_path):
        if '.git' in root:
            continue
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, dir_path)
            file_hashes[relative_path] = calculate_file_hash(file_path)
    return file_hashes

def clone_or_pull_repo(repo_url, local_path):
    """Клонирует или обновляет репозиторий."""
    if os.path.exists(local_path):
        try:
            repo = git.Repo(local_path)
            repo.remotes.origin.pull()
            console.print("[bold green]Репозиторий обновлен.[/bold green]")
        except git.exc.InvalidGitRepositoryError:
            console.print("[bold red]Обнаружен недействительный репозиторий Git. Перезагрузка...[/bold red]")
            repo = git.Repo.clone_from(repo_url, local_path, progress=clone_progress)
            console.print("[bold green]Репозиторий клонирован.[/bold green]")
    else:
        repo = git.Repo.clone_from(repo_url, local_path, progress=clone_progress)
        console.print("[bold green]Репозиторий клонирован.[/bold green]")

def clone_progress(op, cur_count, max_count=None, message=''):
    """Отображает прогресс клонирования репозитория."""
    if max_count is not None:
        progress = cur_count / max_count
        console.print(f"Клонирование: {message} ({cur_count}/{max_count})", end="\r")

def load_exceptions(file_name="exceptions.txt"):
    """Загружает исключения из файла."""
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_exceptions(exceptions, file_name="exceptions.txt"):
    """Сохраняет исключения в файл."""
    with open(file_name, "w") as f:
        for item in exceptions:
            f.write(f"{item}\n")

def load_settings(file_name="settings.json"):
    """Загружает настройки из JSON файла."""
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return {}

def save_settings(settings, file_name="settings.json"):
    """Сохраняет настройки в JSON файл."""
    with open(file_name, "w") as f:
        json.dump(settings, f, indent=4)