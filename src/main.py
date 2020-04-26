from src.gui.main import initialize_gui
from src.task_controller import TaskController

if __name__ == "__main__":

    task_controller = TaskController()
    task_controller.create_connection(database_url="tasks.db")

    initialize_gui(controller=task_controller)

    # ToDO
    task_controller.close_connection()
