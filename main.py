import typer
from pathlib import Path
import json
from datetime import datetime

app = typer.Typer()

DATA_FILE = Path("tasks.json")
STATUSES = ['todo', 'inprogress', 'completed']



def load_tasks():
    """Load tasks from JSON file"""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r") as f:
        return json.load(f)


def save_tasks(tasks):
    """Save tasks to JSON file"""
    with DATA_FILE.open("w") as f:
        json.dump(tasks, f, indent=4)

@app.command()
def add(description: str):
    """Add a new task to the tasks list."""
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo", #default
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    tasks.append(new_task)
    save_tasks(tasks)
    typer.echo(f"Added task {new_task['id']}")

@app.command()
def remove(id: int):
    """Remove a task from the tasks list."""
    tasks = load_tasks()
    tasks.pop(id)
    save_tasks(tasks)
    typer.echo(f"Removed task {id}")
    typer.echo("Done")

@app.command()
def update(id: int, status: str):
    """Update the status of a task."""
    tasks = load_tasks()
    for task in tasks:
        if task["status"] in status:
            task["status"] = status[task["status"]]
            save_tasks(tasks)

if __name__ == "__main__":
    app()