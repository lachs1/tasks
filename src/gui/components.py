import tkinter as tk

from src.task import Task
from src.constants import TASK_BG_COLOR, PLACEHOLDER_COLOR


class TaskElement(tk.Frame):
    def __init__(self, task: Task, master=None):
        """

        :param task: Task Object
        :param master: GUI Object
        """
        super().__init__(master=master)
        self.task = task
        self._checkbox_variable = tk.IntVar()
        self._initialize()

    def _initialize(self) -> None:
        """

        :return: None
        """

        self["bg"] = TASK_BG_COLOR

        self.grid_columnconfigure(index=0)
        self.grid_columnconfigure(index=1, weight=1)
        # self.grid_columnconfigure(index=2)

        self.grid_rowconfigure(index=0)

        check_button = tk.Checkbutton(
            master=self,
            variable=self._checkbox_variable,
            text=self.task.props["text"],
            bg=self["bg"],
        )
        check_button.grid(row=0, column=0)


class TaskListElement(tk.Frame):
    def __init__(self, master=None):
        """

        :param master: GUI Object
        """
        super().__init__(master=master)
        self._initialize()

    def _initialize(self) -> None:
        """

        :return: None
        """
        self.grid_columnconfigure(index=0, weight=1)

    def render_tasks(self) -> None:
        # ToDo: flickering when called.
        """

        :return: None
        """
        for task in self.grid_slaves():
            task.grid_forget()

        for index, task in enumerate(self.master.tasks):
            task_element = TaskElement(task=task, master=self)
            task_element.grid(row=index, column=0, sticky="ew")
            self.grid_rowconfigure(index=index, pad=5)

    def append_task(self, task: Task) -> None:
        """
        :param task: Task Object
        :return: None
        """
        pass


class EntryElement(tk.Entry):
    def __init__(self, master=None, placeholder=None):
        """

        :param master: GUI Object
        :param placeholder: String
        """
        super().__init__(master=master)
        self._placeholder_color = PLACEHOLDER_COLOR
        self._default_color = self["fg"]

        self.placeholder = placeholder
        self.focused = False

        self.bind(sequence="<FocusIn>", func=self._focus_in)
        self.bind(sequence="<FocusOut>", func=self._focus_out)
        self.bind(sequence="<Return>", func=self._append_task)

        self._append_placeholder()

    def _append_placeholder(self) -> None:
        """

        :return: None
        """
        self.focused = False
        self.insert(index=0, string=self.placeholder)
        self["fg"] = self._placeholder_color

    def _append_task(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        text = self.get()
        if text:
            self._clean()
            task = Task(props={"text": text, "due": 4})
            self.master.add_task(task=task)
        else:
            print("empty")
            pass
        self.master.render_tasks()

    def _clean(self):
        self.delete(first="0", last="end")

    def _focus_in(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        if not self.focused:
            self.focused = True
            self._clean()
            self["fg"] = self._default_color

    def _focus_out(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        if not self.get():
            self._append_placeholder()
