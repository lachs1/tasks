from typing import Tuple


class Task(object):
    def __init__(self, date: str, text: str, done: bool = False):
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
    def props(self) -> Tuple[str, str, bool]:
        """

        :return: Tuple of properties
        """
        return self._date, self._text, self._done
