import sqlite3

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
        self._cursor = self._connection.cursor()

    def create_new_table(self, name: str) -> None:
        """

        :param name: Str, table name
        :return: None
        """
        if self._cursor:
            sql_statement = "CREATE TABLE ?(date text, text text, done integer)"
            self._cursor.execute(sql_statement, name)

    def add_task_to_table(self, task: Task, table_name: str) -> None:
        """

        :param task: Task object
        :param table_name: string
        :return: None
        """
        if self._cursor:
            sql_statement = "INSERT INTO {table} VALUES (?, ?, ?)".format(
                table=table_name
            )
            self._cursor.execute(sql_statement, task.props)
            self.commit()

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
