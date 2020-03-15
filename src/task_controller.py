from typing import List, Tuple

from src.task import Task
from src.database_controller import DatabaseController


class TaskController(object):
    def __init__(self, database_controller: DatabaseController):
        """

        :param database_controller: DataBaseController object
        """
        self._database_controller = database_controller

    def add_task(self, task: Task, table_name: str) -> int:
        """
        Method returns an error if it fails to add task to database.
        :param task: Task Object
        :param table_name: Name of current table
        :return: int
        """
        error = self._database_controller.add_task_to_table(
            task=task, table_name=table_name
        )
        if error:
            return 1
        return 0

    def get_tasks(self, table_name: str) -> Tuple[int, List[Task]]:
        """

        :param table_name:
        :return:
        """
        error, tasks = self._database_controller.get_tasks_from_table(table_name=table_name)
        if error:
            return error, tasks
        return error, tasks
