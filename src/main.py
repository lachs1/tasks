from src.database_controller import DatabaseController
from src.gui.main import initialize_gui
from src.task_controller import TaskController

if __name__ == "__main__":

    db_controller = DatabaseController()
    db_controller.create_connection(database_url="tasks.db")

    task_controller = TaskController(database_controller=db_controller)

    initialize_gui(controller=task_controller)

    # ToDO
    db_controller.close_connection()
