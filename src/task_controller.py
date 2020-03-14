from typing import List

from src.task import Task


class TaskController(object):
    def __init__(self, tasks: List[Task]):
        """

        :param tasks: List of Task Objects
        """
        self.tasks = tasks

    def add_task(self, task: Task) -> int:
        """
        Method returns an error if it fails to add task to database.
        :param task: Task Object
        :return: int
        """
        self.tasks.append(task)
        return 1
