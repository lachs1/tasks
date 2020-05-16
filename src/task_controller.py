import sqlite3
from typing import List, Tuple
import re

from src.task import Task
from src.check_list import CheckList


class TaskController(object):
    def __init__(self):
        self._connection = None
        self._cursor = None

    def add_task(self, task: Task) -> Tuple[int, str]:
        """
        1 = Error
        0 = No error
        :param task: Task object
        :return: int
        """
        if self._cursor:
            try:
                sql_statement = """
                                INSERT INTO Tasks (dueDate, description, done, checkListID)
                                VALUES (?, ?, ?, ?);
                                """
                self._cursor.execute(
                    sql_statement,
                    (task.due_date, task.description, task.done, task.check_list_id),
                )
                self.commit()
                return 0, ""
            except sqlite3.Error as e:
                return 1, "Database error: {0}".format(e)
        return 1, "There is no connection."

    def get_tasks(self, check_list_id: int) -> Tuple[int, str, List[Task]]:
        """

        :param check_list_id: Str name of the list
        :return: List of task objects
        """
        if self._cursor:
            try:
                sql_statement = """
                                SELECT * FROM Tasks
                                WHERE checkListID == ?
                                """
                self._cursor.execute(sql_statement, (check_list_id,))
                response = self._cursor.fetchall()
                tasks = []
                for row in response:
                    task = Task(
                        tid=row[0],
                        due_date=row[1],
                        description=row[2],
                        done=row[3],
                        check_list_id=check_list_id,
                    )
                    tasks.append(task)
                return 0, "", tasks
            except sqlite3.Error as e:
                print(e)
                return 1, "Database error: {0}".format(e), []
        return 1, "There is no connection.", []

    def get_check_lists(self) -> Tuple[int, str, List[CheckList]]:
        """

        :return:
        """
        if self._cursor:
            try:
                sql_statement = "SELECT * FROM CheckLists"
                self._cursor.execute(sql_statement)
                response = self._cursor.fetchall()
                check_lists = []
                for row in response:
                    check_list = CheckList(cid=row[0], name=row[1], description=row[2])
                    check_lists.append(check_list)
                return 0, "", check_lists
            except sqlite3.Error as e:
                return 1, "Database error: {0}".format(e), []
        return 1, "There is no connection.", []

    def update_task(self, task: Task) -> Tuple[int, str]:
        """

        :param task:
        :return:
        """
        if self._cursor:
            try:
                sql_statement = """
                                UPDATE Tasks
                                SET dueDate = ?, description = ?, done = ?, checkListID = ?
                                WHERE ID = ?;
                                """
                self._cursor.execute(
                    sql_statement,
                    (
                        task.due_date,
                        task.description,
                        task.done,
                        task.check_list_id,
                        task.tid,
                    ),
                )
                self.commit()
                return 0, ""
            except sqlite3.Error as e:
                return 1, "Database error: {0}".format(e)
        return 1, "There is no connection."

    def create_connection(self, database_url: str, foreign_keys: int = True) -> None:
        """

        :param database_url:
        :param foreign_keys:
        :return:
        """
        self._connection = sqlite3.connect(database_url)
        if foreign_keys:
            self._connection.execute("PRAGMA foreign_keys = 1")
        self._cursor = self._connection.cursor()

    def add_check_list(self, check_list: CheckList) -> Tuple[int, str]:
        """
        """
        if not re.match("^[a-zA-Z0-9_ ]{1,20}$", check_list.name):
            return 1, "Enter a valid list name."

        if self._cursor:
            try:
                sql_statement = (
                    """INSERT INTO CheckLists (name, description) VALUES (?, ?)"""
                )
                self._cursor.execute(
                    sql_statement, (check_list.name, check_list.description)
                )
                self.commit()
            except sqlite3.Error as e:
                return 1, "Database error: {0}".format(e)
            return 0, ""
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

    def create_tasks_table(self) -> None:
        """
        :return:
        """
        try:
            # ToDo: TEXT LENGTH
            sql_statement = """
                            CREATE TABLE IF NOT EXISTS Tasks (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                dueDate DATE,
                                description TEXT NOT NULL,
                                done INTEGER NOT NULL,
                                checkListID INTEGER,
                                FOREIGN KEY (checkListID) REFERENCES CheckLists(ID)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE
                            );
                            """

            self._cursor.execute(sql_statement)
        except sqlite3.Error as e:
            print(e)

    def create_check_lists_table(self) -> None:
        """
        :return:
        """
        try:
            # ToDo: TEXT LENGTH
            sql_statement = """
                            CREATE TABLE IF NOT EXISTS CheckLists (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                description TEXT
                            );
                            """
            self._cursor.execute(sql_statement)
        except sqlite3.Error as e:
            print(e)
