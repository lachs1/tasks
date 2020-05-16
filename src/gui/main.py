import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import Tuple, List

from src.task import Task
from src.check_list import CheckList
from src.task_controller import TaskController

MAIN_BACKGROUND_COLOR = "#1E1E1E"
TASK_ELEMENT_BACKGROUND_COLOR = "#323232"
CHECK_LISTS_BACKGROUND_COLOR = "#302F2F"
ENTRY_BACKGROUND_COLOR = "#262626"
ENTRY_PLACEHOLDER_COLOR = "#d5dcd6"
WHITE_COLOR = "#FFFFFF"


class TasksGUI(tk.Frame):
    def __init__(self, task_controller: TaskController, master: tk.Tk):
        """

        :param task_controller: TaskController Object
        :param master: Tk Object
        """
        super().__init__(master=master)
        self._check_lists_tk = None
        self._canvas_tk = None
        self._tasks_tk = None
        self._entry_tk = None
        self._root_tk = master
        self._task_controller = task_controller
        self._selected_cid = None
        self._initialize()

    def _initialize(self) -> None:
        """

        :return: None
        """
        self._set_window_size_and_pos()

        self._root_tk.grid_columnconfigure(index=0, weight=1)
        self._root_tk.grid_rowconfigure(index=0, weight=1)

        self.grid_columnconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        self._check_lists_tk = CheckLists(master=self)
        self._check_lists_tk.grid(row=0, column=0, sticky="ns")

        self._canvas_tk = tk.Canvas(
            master=self, bd=0, highlightthickness=0, relief="ridge"
        )
        self._tasks_tk = Tasks(master=self)

        scrollbar = tk.Scrollbar(
            master=self, orient="vertical", command=self._canvas_tk.yview,
        )
        self._canvas_tk.configure(
            yscrollcommand=scrollbar.set, scrollregion=self._canvas_tk.bbox("all")
        )
        scrollbar.grid(row=0, column=2, sticky="ns")

        self._canvas_tk.grid(row=0, column=1, sticky="nsew")
        self._task_frame_id = self._canvas_tk.create_window(
            (0, 0), window=self._tasks_tk, anchor="nw"
        )

        self._entry_tk = EntryFrame(master=self)
        self._entry_tk.grid(row=1, column=1, columnspan=2, sticky="ew")

        self._new_list_btn_tk = tk.Button(
            master=self, text="\uFF0B New List", command=self._on_new_list_btn_press
        )
        self._new_list_btn_tk.grid(row=1, column=0, sticky="nsew")

        self.grid(column=0, row=0, sticky="nsew")

        self._check_lists_tk.bind(sequence="<<ListboxSelect>>", func=self._on_list_change)
        self._canvas_tk.bind(sequence="<Configure>", func=self._configure_canvas)
        self._tasks_tk.bind(sequence="<Enter>", func=self._bound_to_mousewheel)
        self._tasks_tk.bind(sequence="<Leave>", func=self._unbound_to_mousewheel)

    def _on_list_change(self, _) -> None:
        """

        :param _:
        :return:
        """
        self._selected_cid = self._check_lists_tk.curselection()[0]
        self._tasks_tk.refresh()

    def _on_new_list_btn_press(self) -> None:
        """
        Called when user clicks "New List" button.
        :return: None
        """
        name = simpledialog.askstring(title="New List", prompt="Name of the new list")
        if name:
            # ToDo: CheckList description
            checklist = CheckList(name=name, description="")
            err, message = self._task_controller.add_check_list(check_list=checklist)
            if err:
                messagebox.showerror(title="Error", message=message)
            else:
                self._check_lists_tk.refresh()

    def _configure_canvas(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        canvas_height = self._canvas_tk.winfo_height()
        frame_height = self._tasks_tk.winfo_reqheight()  # Required height

        if canvas_height >= frame_height:
            new_height = canvas_height
        else:
            new_height = frame_height
        self._canvas_tk.itemconfigure(
            self._task_frame_id, height=new_height, width=self._canvas_tk.winfo_width()
        )

        self._canvas_tk.configure(scrollregion=self._canvas_tk.bbox("all"))

    def _bound_to_mousewheel(self, _) -> None:
        """

        :param _:
        :return: None
        """
        self._canvas_tk.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, _):
        """

        :param _:
        :return: None
        """
        self._canvas_tk.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event) -> None:
        """

        :param event: Tk Event Object
        :return: None
        """
        delta = 1
        if event.num == 5 or event.delta < 0:
            delta = -1
        self._canvas_tk.yview_scroll(delta, "units")

    def _set_window_size_and_pos(self) -> None:
        """

        :return: None
        """
        # ToDO: ?
        # Ensure that the geometry values returned are accurate
        # https://stackoverflow.com/a/10018670
        self._root_tk.update_idletasks()
        screen_width, screen_height = self.get_screen_size()

        window_width = int(round(0.5 * screen_width))
        window_height = int(round(0.4 * screen_height))

        x = screen_width // 2 - window_width // 2
        y = screen_height // 2 - window_height // 2

        self._root_tk.geometry(
            newGeometry="{0}x{1}+{2}+{3}".format(window_width, window_height, x, y)
        )

    def get_screen_size(self) -> Tuple[int, int]:
        """

        :return: Tuple[Width: Int, Height: Int]
        """
        return self._root_tk.winfo_screenwidth(), self._root_tk.winfo_screenheight()

    def add_task(self, task: Task) -> None:
        """

        :param task: Task object
        :return:
        """
        task.check_list_id = self._selected_cid
        error, message = self._task_controller.add_task(task=task)
        if error:
            messagebox.showerror(title="Error", message=message)
        else:
            self._tasks_tk.refresh()

    @property
    def tasks(self) -> List[Task]:
        """

        :return:
        """
        error, message, tasks = self._task_controller.get_tasks(check_list_id=self._selected_cid)
        if error:
            messagebox.showerror(title="Error", message=message)
        return tasks

    @property
    def check_lists(self) -> List[CheckList]:
        """

        :return:
        """
        error, message, lists = self._task_controller.get_check_lists()
        if error:
            messagebox.showerror(title="Error", message=message)
        return lists

    def update_task(self, task: Task) -> None:
        """

        :param task:
        :return:
        """
        error, message = self._task_controller.update_task(task=task)
        if error:
            messagebox.showerror(title="Error", message=message)


class EntryFrame(tk.Frame):
    def __init__(self, master: TasksGUI):
        super().__init__(master=master)
        self._entry = None  # Tk element
        self._task_gui = master  # Tk Element
        self._initialize()

    def _initialize(self) -> None:
        """

        :return: None
        """
        self.configure(bg=MAIN_BACKGROUND_COLOR)

        self.grid_columnconfigure(index=1, weight=1)

        plus_sign = tk.Label(
            master=self,
            text="\uFF0B",
            background=ENTRY_BACKGROUND_COLOR,
            fg=WHITE_COLOR,
            borderwidth=0,
        )
        plus_sign.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="nsew")

        self._entry = EntryElement(master=self, placeholder="Add a task")
        self._entry.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="ew")

    def add_task(self, task: Task) -> None:
        """

        :param task:
        :return: None
        """
        self._task_gui.add_task(task=task)


class Tasks(tk.Frame):
    def __init__(self, master: TasksGUI):
        super().__init__(master=master)
        self._task_gui = master  # Tk Element
        self._initialize()
        self.refresh()

    def _initialize(self) -> None:
        """

        :return: None
        """
        self.configure(bg=MAIN_BACKGROUND_COLOR)

        self.grid_columnconfigure(index=0, weight=1)

    def refresh(self) -> None:
        """
        :return: None
        """
        for task in self.grid_slaves():
            task.grid_forget()

        for index, task in enumerate(self._task_gui.tasks):
            task_element = TaskElement(task=task, master=self)
            task_element.grid(row=index, column=0, pady=(5, 0), padx=5, sticky="ew")

    def update_task(self, task: Task) -> None:
        """

        :param task: Task Object
        :return: None
        """
        self._task_gui.update_task(task=task)


class TaskElement(tk.Checkbutton):
    def __init__(self, task: Task, master: Tasks):
        """

        :param task: Task Object
        :param master: TaskList
        """
        self._task = task
        self._checked = tk.BooleanVar(value=task.done)
        self._task_list = master
        super().__init__(
            master=master,
            state="normal",
            variable=self._checked,
            text=self._task.description,
            anchor="w",
            padx=5,
            pady=5,
            command=self._update_task,
            background=TASK_ELEMENT_BACKGROUND_COLOR,
            fg=WHITE_COLOR,
        )

    def _update_task(self) -> None:
        """

        :return: None
        """
        self._task.done = self._checked.get()
        self._task_list.update_task(task=self._task)


class EntryElement(tk.Entry):
    def __init__(self, master: EntryFrame, placeholder: str):
        """

        :param master: GUI Object
        :param placeholder: String
        """
        # ToDo: validatecommand=
        super().__init__(
            master=master,
            borderwidth=5,
            relief="flat",
            highlightthickness=0,
            bg=ENTRY_BACKGROUND_COLOR,
        )

        self._placeholder_color = ENTRY_PLACEHOLDER_COLOR
        self._default_color = WHITE_COLOR
        self._placeholder = placeholder
        self._entry_frame = master

        self.focused = False

        self.bind(sequence="<FocusIn>", func=self._focus_in)
        self.bind(sequence="<FocusOut>", func=self._focus_out)
        self.bind(sequence="<Return>", func=self._add_task)

        self._insert_placeholder()

    def _insert_placeholder(self) -> None:
        """

        :return: None
        """
        self.focused = False

        self.insert(index=0, string=self._placeholder)
        self.configure(fg=self._placeholder_color)

    def _clean(self) -> None:
        """

        :return: None
        """
        self.delete(first="0", last="end")

    def _focus_in(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        if not self.focused:
            self.focused = True
            self._clean()
            self.configure(fg=self._default_color)

    def _focus_out(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        if not self.get():
            self._insert_placeholder()

    def _add_task(self, _) -> None:
        """

        :param _: Tk Event Object
        :return: None
        """
        text = self.get()
        if text:
            self._clean()
            # ToDo: List_name
            self._entry_frame.add_task(task=Task(description=text))


class CheckLists(tk.Listbox):
    def __init__(self, master: TasksGUI):
        super().__init__(
            master=master,
            borderwidth=0,
            highlightthickness=0,
            activestyle=None,
            background=CHECK_LISTS_BACKGROUND_COLOR,
            font=("Helvetica", 20),
            width=15,
            highlightcolor=None,
            selectbackground=None,
            fg=WHITE_COLOR,
        )
        self._task_gui_tk = master
        self.refresh()
        self.select_set(0)

    def refresh(self) -> None:
        """

        :return:
        """
        self.delete(0, 'end')

        check_lists = self._task_gui_tk.check_lists

        for check_list in check_lists:
            self.insert("end", check_list.name)


def initialize_gui(task_controller: TaskController) -> None:
    """

    :param task_controller: TaskController Object
    :return: None
    """

    root = tk.Tk()
    root.title("Tasks")

    icon = tk.Image(imgtype="photo", file="src/ico.png")
    root.iconphoto(True, icon)

    _ = TasksGUI(master=root, task_controller=task_controller)

    root.mainloop()
