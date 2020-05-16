
class Task(object):
    def __init__(
        self,
        description: str,
        due_date: str = "",
        check_list_id: int = None,
        done: bool = False,
        tid: int = None,
    ):
        """
        :param check_list_id:
        :param due_date: Due date of the task
        :param description: Description of the task
        :param done: Done Flag
        :param tid: Task Id
        """
        self._check_list_id = check_list_id
        self._due_date = due_date
        self._description = description
        self._done = done
        self._tid = tid

    @property
    def check_list_id(self) -> int:
        """

        :return:
        """
        return self._check_list_id

    @check_list_id.setter
    def check_list_id(self, cid: int) -> None:
        """

        :return:
        """
        self._check_list_id = cid

    @property
    def description(self) -> str:
        """

        :return: str
        """
        return self._description

    @property
    def done(self) -> bool:
        """

        :return: bool
        """
        return self._done

    @done.setter
    def done(self, val: bool) -> None:
        """

        :param val:
        :return: None
        """
        self._done = val

    @property
    def tid(self) -> int:
        """

        :return: int
        """
        return self._tid

    @property
    def due_date(self) -> str:
        """

        :return: str
        """
        return self._due_date
