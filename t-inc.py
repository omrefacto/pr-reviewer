import datetime

class Task:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.created_at = datetime.datetime.now()
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "✔️ Done" if self.completed else "❌ Pending"
        return f"{self.title} - {status}\n   {self.description}\n   Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description=""):
        task = Task(title, description)
        self.tasks.append(task)
        print(f"Task '{title}' added successfully!\n")

    def mark_task_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()
            print(f"Task '{self.tasks[index].title}' marked as complete!\n")
        else:
            print("Invalid task number.\n")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            print(f"Task '{removed.title}' deleted successfully!\n")
        else:
            print("Invalid task number.\n")


def display_menu():
    print("========== TO-DO LIST ==========")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Complete")
    print("4. Delete Task")
    print("5. Exit")
    print("================================")


def main():
    todo = ToDoList()

    while True:
        display_menu()
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            todo.add_task(title, description)

        elif choice == "3":
            todo.view_tasks()
            try:
                index = int(input("Enter task number to mark complete: ")) - 1
                todo.mark_task_complete(index)
            except ValueError:
                print("Please enter a valid number.\n")

        elif choice == "4":
            todo.view_tasks()
            try:
                index = int(input("Enter task number to delete: ")) - 1
                todo.delete_task(index)
            except ValueError:
                print("Please enter a valid number.\n")

        elif choice == "5":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid option, try again.\n")


if __name__ == "__main__":
    main()
