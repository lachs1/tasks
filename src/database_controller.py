import sqlite3
from typing import List, Tuple

from src.task import Task


class DatabaseController(object):
    def __init__(self):
        self._connection = None
        self._cursor = None

    def create_connection(self, database_url: str) -> None:
        """

        :param database_url:
        :return:
        """
        self._connection = sqlite3.connect(database_url)
        # https://stackoverflow.com/a/41920171
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()

    def create_new_table(self, name: str) -> None:
        """

        :param name: Str, table name
        :return: None
        """
        if self._cursor:
            sql_statement = "CREATE TABLE ?(date text, text text, done integer)"
            self._cursor.execute(sql_statement, name)

    def add_task_to_table(self, task: Task, table_name: str) -> int:
        """

        :param task: Task object
        :param table_name: string
        :return: int
        """
        if self._cursor:
            try:
                sql_statement = "INSERT INTO {table} VALUES (?, ?, ?)".format(
                    table=table_name
                )
                self._cursor.execute(sql_statement, task.props)
                self.commit()
                return 0
            except sqlite3.Error as e:
                print("Database error: %s" % e)
                return 1
        else:
            return 1

    def get_tasks_from_table(self, table_name: str) -> Tuple[int, List[Task]]:
        """

        :param table_name: Str table name
        :return: List of task objects
        """
        if self._cursor:
            try:
                sql_statement = "SELECT * FROM {table}".format(table=table_name)
                self._cursor.execute(sql_statement)
                response = (dict(row) for row in self._cursor.fetchall())
                # ToDo: tasks generator or list?
                tasks = [Task(**task) for task in response]
                return 0, tasks
            except sqlite3.Error as e:
                print("Database error: %s" % e)
                return 1, []
        else:
            return 1, []

    def commit(self) -> None:
        """

        :return: None
        """
        self._connection.commit()

    def close_connection(self) -> None:
        """

        :return: None
        """
        self._connection.close()
