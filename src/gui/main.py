import tkinter as tk
from typing import Tuple

from src.gui.components import ButtonMapElement, EntryElement, TaskListElement
from src.task import Task
from src.task_controller import TaskController


class GUI(tk.Frame):
    def __init__(self, controller, master=None):
        """

        :param master: Tk Object
        """
        super().__init__(master=master)
        self._task_list = None  # Tk
        self._controller = controller
        self._initialize()
        self.render_tasks()

    def _initialize(self) -> None:
        """

        :return: None
        """
        self._set_window_size_and_pos()

        self.master.grid_columnconfigure(index=0, weight=1)
        self.master.grid_rowconfigure(index=0, weight=1)

        self.grid_columnconfigure(index=0, weight=1)

        self.grid_rowconfigure(index=0, pad=5)
        self.grid_rowconfigure(index=1, pad=5, weight=1)
        self.grid_rowconfigure(index=2, pad=5)

        entry = EntryElement(master=self, placeholder="Enter task to list 'todos'")
        entry.grid(row=0, column=0, sticky="ew")

        self._task_list = TaskListElement(master=self)
        self._task_list.grid(row=1, column=0, sticky="nsew")

        button_map = ButtonMapElement(master=self)
        button_map.grid(row=2, column=0, sticky="s")

        self.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")

    def _set_window_size_and_pos(self) -> None:
        """

        :return: None
        """
        # Ensure that the geometry values returned are accurate
        # https://stackoverflow.com/a/10018670
        self.master.update_idletasks()
        screen_width, screen_height = self.get_screen_size()

        window_width = int(round(0.15 * screen_width))
        window_height = int(round(0.30 * screen_height))

        x = screen_width // 2 - window_width // 2
        y = screen_height // 2 - window_height // 2

        self.master.geometry(
            newGeometry="{0}x{1}+{2}+{3}".format(window_width, window_height, x, y)
        )

    def render_tasks(self) -> None:
        """

        :return: None
        """
        self._task_list.render_tasks()

    def get_screen_size(self) -> Tuple[int, int]:
        """

        :return: Tuple[Width: Int, Height: Int]
        """
        return self.master.winfo_screenwidth(), self.master.winfo_screenheight()

    def add_task(self, task: Task) -> None:
        """

        :param task:
        :return:
        """
        self._controller.add_task(task=task)

    @property
    def tasks(self):
        """

        :return:
        """
        return self._controller.tasks


def initialize_gui(controller: TaskController) -> None:
    """

    :param controller: TaskController Object
    :return: None
    """
    root = tk.Tk()
    _ = GUI(master=root, controller=controller)
    root.mainloop()
