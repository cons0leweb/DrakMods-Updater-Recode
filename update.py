import os
import shutil
from rich.progress import Progress
from rich.console import Console
from utils import get_files_hashes, calculate_file_hash, clone_or_pull_repo

console = Console()

def check_and_update_files(base_path, repo_url):
    """Проверяет и обновляет файлы."""
    temp_repo_path = os.path.join(base_path, "updatefiles_repo")
    os.makedirs(temp_repo_path, exist_ok=True)
    clone_or_pull_repo(repo_url, temp_repo_path)

    repo_files_hashes = get_files_hashes(temp_repo_path)

    updated_files = 0
    total_files = len(repo_files_hashes)

    with Progress() as progress:
        task = progress.add_task("[cyan]Проверка файлов...", total=total_files)

        for file_path, repo_hash in repo_files_hashes.items():
            progress.update(task, advance=1, description=f"[cyan]Проверка: {file_path}")

            local_file_path = os.path.join(base_path, file_path)
            repo_file_path = os.path.join(temp_repo_path, file_path)

            if not os.path.exists(local_file_path) or calculate_file_hash(local_file_path) != repo_hash:
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                shutil.copy2(repo_file_path, local_file_path)
                updated_files += 1
                console.print(f"[bold green]Обновлено: {local_file_path}[/bold green]")

    console.print(f"[bold green]Обновление завершено. Обновлено {updated_files}/{total_files} файлов.[/bold green]")