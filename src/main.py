from typing import Tuple
import time

from src.taskcontroller import TaskController
from src.task import Task
from src.gui.main import initialize_gui


def create_task_controller(database_url: str) -> Tuple[bool, TaskController]:
    """
    Function fetches all tasks from database.
    :return: Tuple[int, object: TaskController]
    """

    # Simulate connection
    print("Connecting to database...")
    time.sleep(1)
    response = [
        {"text": "Buy milk", "due": 1, "done": False},
        {"text": "Read a book", "due": 2, "done": False},
        {"text": "Clean", "due": 3, "done": False},
    ]
    if response:
        print("Successfully fetched tasks!")
    tasks = [Task(props=props) for props in response]
    return False, TaskController(tasks=tasks)


if __name__ == "__main__":
    error, controller = create_task_controller("")
    if error:
        print(error)
        pass
    else:
        initialize_gui(controller=controller)
