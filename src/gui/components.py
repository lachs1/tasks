import tkinter as tk
from typing import Callable

from src.constants import MORE_IMAGE, PLACEHOLDER_COLOR, SORT_IMAGE, TASK_BG_COLOR
from src.task import Task


class TaskElementCheckButton(tk.Checkbutton):
    def __init__(self, master, text: str):
        self._checked = tk.BooleanVar(value=False)
        if master.task.done:
            self._checked.set(value=True)
        self._text = text
        super().__init__(
            master=master,
            variable=self._checked,
            text=self._text,
            bg=master["bg"],
            command=self._on_click,
        )

    def _on_click(self) -> None:
        """

        :return:
        """
        # ToDo: logic
        self.master.task.done = self._checked.get()
        self.master.update_task(task=self.master.task)


class TaskElement(tk.Frame):
    def __init__(self, task: Task, master):
        """

        :param task: Task Object
        :param master: GUI Object
        """
        super().__init__(master=master)
        self.task = task
        self.update_task = self.master.update_func  # ref
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

        check_button = TaskElementCheckButton(master=self, text=self.task.text)
        check_button.grid(row=0, column=0)


class TaskListElement(tk.Frame):
    def __init__(self, master, update_func: Callable):
        """

        :param master: GUI Object
        """
        super().__init__(master=master)
        self.update_func = update_func
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

        for index, task in enumerate(self.master.get_tasks()):
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
            # ToDo: proper task object generating
            task = Task(date="", text=text)
            self.master.add_task(task=task)
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


class ButtonMapElement(tk.Frame):
    def __init__(self, master):
        """

        :param master: Tk GUI Object
        """
        super().__init__(master=master)
        self._initialize()

    def _initialize(self) -> None:
        """

        :return: None
        """

        self.grid_columnconfigure(index=0, pad=5)
        self.grid_columnconfigure(index=1, pad=5)

        sort_image = tk.PhotoImage(file=SORT_IMAGE)
        more_image = tk.PhotoImage(file=MORE_IMAGE)

        sort_button = ImageButtonWithText(master=self, image=sort_image, text="Sort")
        more_button = ImageButtonWithText(master=self, image=more_image, text="More")

        sort_button.grid(row=0, column=0, padx=10)
        more_button.grid(row=0, column=1, padx=10)


class ImageButtonWithText(tk.Frame):
    def __init__(self, master, image, text):
        super().__init__(master=master)
        self._image = image
        self._text = text
        self._initialize()
        self.bind(sequence="<Enter>", func=self._on_enter)
        self.bind(sequence="<Leave>", func=self._on_leave)

    def _initialize(self) -> None:
        """

        :return: None
        """
        image_label = tk.Label(master=self, image=self._image)
        text_label = tk.Label(master=self, text=self._text)

        image_label.grid(row=0, column=0)
        text_label.grid(row=1, column=0)

    def _on_enter(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        pass

    def _on_leave(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        pass
