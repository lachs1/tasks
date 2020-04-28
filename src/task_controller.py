import sqlite3
from typing import List, Tuple
import re

from src.task import Task


class TaskController(object):
    def __init__(self):
        self._connection = None
        self._cursor = None

    def add_task(self, task: Task, table_name: str) -> int:
        """
        Method returns an error if it fails to add task to database.
        1 = Error
        0 = No error
        :param task: Task object
        :param table_name: string
        :return: int
        """
        if self._cursor:
            try:
                sql_statement = "INSERT INTO {table}(date, text, done) VALUES (?, ?, ?)".format(
                    table=table_name
                )
                self._cursor.execute(sql_statement, task.props_no_tid)
                self.commit()
                return 0
            except sqlite3.Error as e:
                print("Database error: %s" % e)
                return 1
        return 1

    def get_tasks(self, table_name: str) -> Tuple[int, List[Task]]:
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
        return 1, []

    def update_task(self, task: Task, table_name: str) -> int:
        """

        :param task:
        :param table_name:
        :return:
        """
        if self._cursor:
            try:
                sql_statement = "UPDATE {table} SET date = ?, text = ?, done = ? WHERE tid = ?".format(
                    table=table_name
                )
                self._cursor.execute(sql_statement, (*task.props_no_tid, task.tid))
                self.commit()
                return 0
            except sqlite3.Error as e:
                print("Database error: %s" % e)
                return 0
        return 1

    def create_connection(self, database_url: str) -> None:
        """

        :param database_url:
        :return:
        """
        self._connection = sqlite3.connect(database_url)
        # https://stackoverflow.com/a/41920171
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()

    def create_new_list(self, list_name: str) -> Tuple[int, str]:
        """
        """
        if self._cursor:
            if re.match(r"(?![\d])(?!sqlite_)\b([\w\d]+)\b", list_name):
                sql_statement = """CREATE TABLE {table} (
                                tid INTEGER PRIMARY KEY AUTOINCREMENT,
                                date text,
                                text text,
                                done integer
                                );""".format(
                    table=list_name
                )
                self._cursor.execute(sql_statement)
                return 0, ""
            return 1, "Please enter a valid list name."
        return 1, "There is no connection."

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
