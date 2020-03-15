from typing import Tuple


class Task(object):
    def __init__(self, date: str, text: str, done: bool = False, tid: int = None):
        self._tid = tid
        self._date = date
        self._text = text
        self._done = done

    @property
    def text(self) -> str:
        """

        :return: str
        """
        return self._text

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
    def props(self) -> Tuple[int, str, str, bool]:
        """

        :return: Tuple of properties
        """
        return self._tid, self._date, self._text, self._done

    @property
    def props_no_tid(self) -> Tuple[str, str, bool]:
        """

        :return: Tuple of properties without task id
        """
        return self._date, self._text, self._done
