from src.gui.main import initialize_gui
from src.task_controller import TaskController
from src.task import Task
from src.check_list import CheckList

if __name__ == "__main__":

    task_controller = TaskController()
    task_controller.create_connection(database_url="pytasks.db")

    initialize_gui(task_controller=task_controller)

    # ToDO
    # task_controller.create_check_lists_table()
    # task_controller.create_tasks_table()

    # check_list = CheckList(name="School", description="School stuff")

    # task = Task(check_list_id=2, description="Testing", due_date="2019-12-12", done=False, tid=1)

    # print(task_controller.create_new_check_list(check_list=check_list))
    # print(task_controller.add_task(task))

    task_controller.close_connection()
