from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from utils import load_exceptions, save_exceptions, load_settings, save_settings
from update import check_and_update_files

console = Console()

def main():
    settings = load_settings()
    base_path = settings.get("base_path", "")
    repo_url = "https://github.com/darvin7531/darkmods.git"

    console.print("[bold blue]Добро пожаловать в DarkMods Updater[/bold blue]")

    if not base_path:
        base_path = Prompt.ask("Введите базовый путь к директории")
        settings["base_path"] = base_path
        save_settings(settings)

    check_and_update_files(base_path, repo_url)

    console.print("[bold blue]Управление списком исключений[/bold blue]")
    exceptions = load_exceptions()

    table = Table(title="Список исключений")
    table.add_column("Путь к файлу")

    for exception in exceptions:
        table.add_row(exception)

    console.print(table)

    add_exception = Prompt.ask("Хотите добавить исключение? (y/n)")
    if add_exception.lower() == "y":
        new_exception = Prompt.ask("Введите путь к файлу для добавления в список исключений")
        exceptions.append(new_exception)
        save_exceptions(exceptions)
        console.print(f"[bold green]Добавлено в список исключений: {new_exception}[/bold green]")