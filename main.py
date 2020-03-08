from typing import Tuple, List
import tkinter as tk
import time

TASK_BG_COLOR = "#bdc3c7"
PLACEHOLDER_COLOR = "#7f8c8d"


class Task(object):
    def __init__(self, props: dict):
        self.props = props


class TaskController(object):
    def __init__(self, tasks: List[Task]):
        """

        :param tasks: List of Task Objects
        """
        self.tasks = tasks

    def add_task(self, task: Task) -> int:
        """
        Method returns an error if it fails to add task to database.
        :param task: Task Object
        :return: int
        """
        self.tasks.append(task)
        return 1


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

        for index, task in enumerate(controller.tasks):
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
            controller.add_task(task=task)
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


class GUI(tk.Frame):
    def __init__(self, master=None):
        """

        :param master: Tk Object
        """
        super().__init__(master=master)
        self.task_list = None
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

        entry = EntryElement(master=self, placeholder="Enter task to list 'todos'")
        entry.grid(row=0, column=0, sticky="ew")

        self.task_list = TaskListElement(master=self)
        self.task_list.grid(row=1, column=0, sticky="nsew")

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
        self.task_list.render_tasks()

    def get_screen_size(self) -> Tuple[int, int]:
        """

        :return: Tuple[Width: Int, Height: Int]
        """
        return self.master.winfo_screenwidth(), self.master.winfo_screenheight()


def create_task_controller(database_url: str) -> Tuple[bool, TaskController]:
    """
    Function fetches all tasks from database.
    :return: Tuple[int, object: TaskController]
    """

    # Simulate connection
    print("Connecting to database...")
    time.sleep(1)
    response = [
        {"text": "Buy milk", "due": 1},
        {"text": "Read a book", "due": 2},
        {"text": "Clean", "due": 3},
    ]
    if response:
        print("Successfully fetched tasks!")
    tasks = [Task(props=props) for props in response]
    return False, TaskController(tasks=tasks)


if __name__ == "__main__":
    error, controller = create_task_controller("")
    if error:
        print(error)
        pass
    else:
        root = tk.Tk()
        app = GUI(master=root)
        root.mainloop()
