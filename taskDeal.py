import datetime as dt
from plyer import notification
import time
import tkinter as tk
from tkinter import messagebox

DAY_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M:%S"


class Tasks:
    def __init__(self, task, date=None, time=None):
        self.task = task

        if date:
            self.date = dt.datetime.strptime(date, DAY_FORMAT).date()
        else:
            self.date = dt.datetime.now().date()

        if time:
            self.time = dt.datetime.strptime(time, TIME_FORMAT).time()
        else:
            self.time = (dt.datetime.now() + dt.timedelta(hours=2)).time()

    def get_info(self):
        return f"Задача: {self.task}\nДата: {self.date.strftime(DAY_FORMAT)}\nВремя: {self.time.strftime(TIME_FORMAT)}"


def remove_task(tasks_list, index):
    del tasks_list[index]


def check_notifications(tasks_list):
    current_datetime = dt.datetime.now()

    for i, task in enumerate(tasks_list):
        task_datetime = dt.datetime.combine(task.date, task.time)

        if current_datetime >= task_datetime:
            show_notification(task.get_info(), task_datetime)
            remove_task(tasks_list, i)
            break  # Stop after handling one notification to avoid issues with the loop


def show_notification(message, start_time):
    notification.notify(
        title="Время выполнить задачу!",
        message=message,
        app_icon=None,
        timeout=10,
    )


def add_task(tasks_list, entry_name, entry_date, entry_time):
    task_name = entry_name.get()
    task_date = entry_date.get()
    task_time = entry_time.get()

    if not task_name or not task_date or not task_time:
        messagebox.showwarning("Предупреждение", "Заполните все поля")
        return

    new_task = Tasks(task_name, date=task_date, time=task_time)
    tasks_list.append(new_task)

    entry_name.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_time.delete(0, tk.END)


def display_tasks(tasks_list):
    if not tasks_list:
        messagebox.showinfo("Информация", "Нет предстоящих задач.")
        return

    tasks_info = "\n\n".join(task.get_info() for task in tasks_list)
    messagebox.showinfo("Предстоящие задачи", tasks_info)


def main():
    tasks_list = []

    root = tk.Tk()
    root.title("Менеджер задач")

    label_name = tk.Label(root, text="Задача:")
    label_date = tk.Label(root, text="Дата (DD.MM.YYYY):")
    label_time = tk.Label(root, text="Время (HH:MM:SS):")

    entry_name = tk.Entry(root)
    entry_date = tk.Entry(root)
    entry_time = tk.Entry(root)

    button_add = tk.Button(
        root,
        text="Добавить задачу",
        command=lambda: add_task(tasks_list, entry_name, entry_date, entry_time),
    )
    button_display = tk.Button(
        root, text="Показать задачи", command=lambda: display_tasks(tasks_list)
    )

    label_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    label_date.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    label_time.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    entry_date.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    entry_time.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    button_add.grid(row=3, column=0, columnspan=2, pady=10)
    button_display.grid(row=4, column=0, columnspan=2, pady=10)

    def check_notifications_loop():
        check_notifications(tasks_list)
        root.after(10000, check_notifications_loop)

    root.after(
        10000, check_notifications_loop
    )  # Start checking notifications after 10 seconds
    root.mainloop()


if __name__ == "__main__":
    main()
