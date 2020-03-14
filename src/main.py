import time
from typing import Tuple

from src.database_controller import DatabaseController
from src.gui.main import initialize_gui
from src.task import Task
from src.task_controller import TaskController


def create_task_controller(database_url: str) -> Tuple[bool, TaskController]:
    """
    Function fetches all tasks from database.
    :return: Tuple[int, object: TaskController]
    """

    # Simulate connection
    print("Connecting to database...")
    time.sleep(1)
    response = [
        {"text": "Buy milk", "date": "", "done": False},
        {"text": "Read a book", "date": "", "done": False},
        {"text": "Clean", "date": "", "done": False},
    ]
    if response:
        print("Successfully fetched tasks!")
    tasks = [Task(**row) for row in response]
    return False, TaskController(tasks=tasks)


if __name__ == "__main__":

    db_controller = DatabaseController()
    db_controller.create_connection(database_url="tasks.db")

    k = Task(date="2018-1-1", text="Testing")
    db_controller.add_task_to_table(task=k, table_name="tasks")

    error, controller = create_task_controller("")
    if error:
        print(error)
        pass
    else:
        initialize_gui(controller=controller)

    db_controller.close_connection()
