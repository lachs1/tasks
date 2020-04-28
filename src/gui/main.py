import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import Tuple, List

from src.task import Task
from src.task_controller import TaskController


class TasksGUI(tk.Frame):
    def __init__(self, controller: TaskController, master: tk.Tk):
        """

        :param master: Tk Object
        """
        super().__init__(master=master)
        self._controller = controller  # TaskController Object
        self._table_list = None  # TK Element
        self._canvas = None  # Tk Element
        self._task_frame = None  # TK Element
        self._entry_frame = None  # Tk Element
        self._root = master  # Tk Element
        self._initialize()
        self.update_all()

    def _initialize(self) -> None:
        """

        :return: None
        """
        self._set_window_size_and_pos()

        self._root.grid_columnconfigure(index=0, weight=1)
        self._root.grid_rowconfigure(index=0, weight=1)

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        self._table_list = TableList(master=self)
        self._table_list.grid(row=0, column=0, sticky="ns")

        self._canvas = tk.Canvas(
            master=self, bd=0, highlightthickness=0, relief="ridge"
        )
        self._task_frame = TaskFrame(master=self)

        scrollbar = tk.Scrollbar(
            master=self, orient="vertical", command=self._canvas.yview,
        )
        self._canvas.configure(
            yscrollcommand=scrollbar.set, scrollregion=self._canvas.bbox("all")
        )
        scrollbar.grid(row=0, column=2, sticky="ns")

        self._canvas.grid(row=0, column=1, sticky="nsew")
        self._task_frame_id = self._canvas.create_window(
            (0, 0), window=self._task_frame, anchor="nw"
        )

        self._entry_frame = EntryFrame(master=self)
        self._entry_frame.grid(row=1, column=1, columnspan=2, sticky="ew")

        self._new_list_btn_tk = tk.Button(master=self, text="\uFF0B New List", command=self._on_new_list_btn_press)
        self._new_list_btn_tk.grid(row=1, column=0, sticky="nsew")

        self.grid(column=0, row=0, sticky="nsew")

        self._canvas.bind(sequence="<Configure>", func=self._configure_canvas)
        self._task_frame.bind(sequence="<Enter>", func=self._bound_to_mousewheel)
        self._task_frame.bind(sequence="<Leave>", func=self._unbound_to_mousewheel)

    def _on_new_list_btn_press(self) -> None:
        """
        Called when user clicks "New List" button.
        :return: None
        """
        name = simpledialog.askstring(title="New List", prompt="Name of the new list")
        err, message = self._controller.create_new_list(list_name=name)
        if err:
            messagebox.showerror(title="Error", message=message)

    def _configure_canvas(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        canvas_height = self._canvas.winfo_height()
        frame_height = self._task_frame.winfo_reqheight()  # Required height

        if canvas_height >= frame_height:
            new_height = canvas_height
        else:
            new_height = frame_height
        self._canvas.itemconfigure(
            self._task_frame_id, height=new_height, width=self._canvas.winfo_width()
        )

        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _bound_to_mousewheel(self, _) -> None:
        """

        :param _:
        :return: None
        """
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, _):
        """

        :param _:
        :return: None
        """
        self._canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event) -> None:
        """

        :param event: Tk Event Object
        :return: None
        """
        delta = 1
        if event.num == 5 or event.delta < 0:
            delta = -1
        self._canvas.yview_scroll(delta, "units")

    def _set_window_size_and_pos(self) -> None:
        """

        :return: None
        """
        # Ensure that the geometry values returned are accurate
        # https://stackoverflow.com/a/10018670
        self._root.update_idletasks()
        screen_width, screen_height = self.get_screen_size()

        window_width = int(round(0.20 * screen_width))
        window_height = int(round(0.30 * screen_height))

        x = screen_width // 2 - window_width // 2
        y = screen_height // 2 - window_height // 2

        self._root.geometry(
            newGeometry="{0}x{1}+{2}+{3}".format(window_width, window_height, x, y)
        )

    def get_screen_size(self) -> Tuple[int, int]:
        """

        :return: Tuple[Width: Int, Height: Int]
        """
        return self._root.winfo_screenwidth(), self._root.winfo_screenheight()

    def append_task(self, task: Task) -> None:
        """

        :param task: Task object
        :return:
        """
        error = self._controller.add_task(task=task, table_name="tasks")
        if error:
            print("Error adding task.")

    def get_tasks(self) -> List[Task]:
        """

        :return:
        """
        error, tasks = self._controller.get_tasks(table_name="tasks")
        if error:
            print("Error fetching tasks.")
        return tasks

    def update_task(self, task: Task) -> None:
        """

        :param task:
        :return:
        """
        error = self._controller.update_task(task=task, table_name="tasks")
        if error:
            print("Error while marking task as one.")

    def update_all(self) -> None:
        """

        :return: None
        """
        self._task_frame.update_all()


class EntryFrame(tk.Frame):
    def __init__(self, master: TasksGUI):
        super().__init__(master=master)
        self._entry = None  # Tk element
        self["bg"] = "#1E1E1E"
        self._initialize()

    def _initialize(self) -> None:
        """

        :return: None
        """
        self.grid_columnconfigure(index=1, weight=1)

        plus_sign = tk.Label(
            master=self, text="\uFF0B", background="#262626", fg="#fff", borderwidth=0,
        )
        plus_sign.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="nsew")

        self._entry = EntryElement(master=self, placeholder="Add a task")
        self._entry.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="ew")


class TaskFrame(tk.Frame):
    def __init__(self, master: TasksGUI):
        super().__init__(master=master)
        self._task_gui = master  # Tk Element
        self._task_list = None  # Tk Element
        self._initialize()
        self["bg"] = "#1E1E1E"

    def _initialize(self) -> None:
        """

        :return: None
        """

        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        self._task_list = TaskListElement(master=self)
        self._task_list.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def add_task(self, task: Task) -> None:
        """

        :return: None
        """
        self._task_gui.append_task(task=task)

    def update_task(self, task: Task) -> None:
        """

        :return: None
        """
        self._task_gui.update_task(task=task)

    def update_all(self) -> None:
        """

        :return: None
        """
        # self._entry.update()  # ToDo?
        self._task_list.render_tasks()


class TaskListElement(tk.Frame):
    def __init__(self, master: TaskFrame):
        """

        :param master: GUI Object
        """
        super().__init__(master=master)
        self._initialize()
        self["bg"] = "#1E1E1E"

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

        for index, task in enumerate(self.master.master.get_tasks()):
            task_element = TaskElement(task=task, master=self)
            task_element.grid(row=index, column=0, sticky="ew")
            self.grid_rowconfigure(index=index, pad=5)

    def update_task(self, task: Task) -> None:
        """

        :return: None
        """
        self.master.update_task(task=task)


class TaskElement(tk.Checkbutton):
    def __init__(self, task: Task, master: TaskListElement):
        """

        :param task: Task Object
        :param master: GUI Object
        """
        self._task = task
        self._checked = tk.BooleanVar(value=(True if task.done else False))
        super().__init__(
            master=master,
            state="normal",
            variable=self._checked,
            text=self._task.text,
            anchor="w",
            padx=5,
            pady=5,
            # ToDo: think about this
            command=self._update_task,
            background="#323232",
            fg="#fff",
        )

    def _update_task(self) -> None:
        """

        :return: None
        """

        self.master.update_task(task=self._task)


class EntryElement(tk.Entry):
    def __init__(self, master: EntryFrame, placeholder: str):
        """

        :param master: GUI Object
        :param placeholder: String
        """
        # ToDo: validatecommand=
        super().__init__(
            master=master, borderwidth=5, relief="flat", highlightthickness=0
        )
        self["bg"] = "#262626"
        self._placeholder_color = "#d5dcd6"
        self._default_color = "#fff"
        self._placeholder = placeholder
        self._task_frame = master
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
        self.insert(index=0, string=self._placeholder)
        self["fg"] = self._placeholder_color

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
            self._task_frame.add_task(task=task)


class TableList(tk.Listbox):
    def __init__(self, master: TasksGUI):
        super().__init__(
            master=master,
            borderwidth=0,
            highlightthickness=0,
            activestyle=None,
            background="#302F2F",
            font=("Helvetica", 20),
            width=15,
            highlightcolor=None,
            selectbackground=None,
            fg="#fff",
        )
        self._initialize()

    def _initialize(self) -> None:
        """

        :return: None
        """
        self.insert("end", "\u2630 School stuff")


def initialize_gui(controller: TaskController) -> None:
    """

    :param controller: TaskController Object
    :return: None
    """
    root = tk.Tk()
    root.title("Tasks")
    #  root.option_add(pattern="*Font", value="courier")
    icon = tk.Image(imgtype="photo", file="src/ico.png")
    root.iconphoto(True, icon)
    _ = TasksGUI(master=root, controller=controller)
    root.mainloop()
