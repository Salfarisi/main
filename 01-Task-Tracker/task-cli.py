import json
import os
import sys
from datetime import datetime

# Nama file JSON yang akan digunakan untuk menyimpan data
TASKS_FILE = 'tasks.json'


def load_tasks():
    """Membaca dan memuat data tugas dari file JSON."""
    if not os.path.exists(TASKS_FILE):
        # Jika file JSON tidak ada, buat file baru dengan format JSON yang valid (array kosong)
        with open(TASKS_FILE, 'w') as file:
            json.dump([], file)
        return []
    
    with open(TASKS_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # Jika file JSON rusak, buat file baru dengan format JSON yang valid
            with open(TASKS_FILE, 'w') as file:
                json.dump([], file)
            return []


def save_tasks(tasks):
    """Menyimpan data tugas ke file JSON."""
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


def add_task(description):
    """Menambahkan tugas baru."""
    tasks = load_tasks()
    task_id = len(tasks) + 1
    task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added successfully (ID: {task_id})')


def update_task(task_id, new_description):
    """Mengupdate deskripsi tugas yang ada."""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['description'] = new_description
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f'Task updated successfully (ID: {task_id})')
    else:
        print(f'Task with ID {task_id} not found')


def delete_task(task_id):
    """Menghapus tugas berdasarkan ID."""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        tasks = [t for t in tasks if t['id'] != task_id]
        save_tasks(tasks)
        print(f'Task deleted successfully (ID: {task_id})')
    else:
        print(f'Task with ID {task_id} not found')


def mark_in_progress(task_id):
    """Menandai tugas sebagai in-progress."""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['status'] = 'in-progress'
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f'Task marked as in-progress (ID: {task_id})')
    else:
        print(f'Task with ID {task_id} not found')


def mark_done(task_id):
    """Menandai tugas sebagai done."""
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['status'] = 'done'
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f'Task marked as done (ID: {task_id})')
    else:
        print(f'Task with ID {task_id} not found')


def list_tasks(status=None):
    """Menampilkan semua tugas, atau tugas berdasarkan status tertentu."""
    tasks = load_tasks()
    if status:
        tasks = [t for t in tasks if t['status'] == status]
    
    if tasks:
        print(f'{"ID":<5} | {"Description":<30} | {"Status":<12} | {"Created At":<25} | {"Updated At":<25}')
        print('-' * 85)
        for task in tasks:
            print(f"{task['id']:<5} | {task['description']:<30} | {task['status']:<12} | {task['createdAt']:<25} | {task['updatedAt']:<25}")
    else:
        print("No tasks found")


def show_menu():
    """Menampilkan daftar fitur yang tersedia untuk pengguna."""
    print("\n*** Welcome to Task Tracker CLI ***")
    print("Available Commands:")
    print("1. add <description> - Add a new task")
    print("2. update <id> <new_description> - Update an existing task")
    print("3. delete <id> - Delete a task")
    print("4. mark-in-progress <id> - Mark a task as in-progress")
    print("5. mark-done <id> - Mark a task as done")
    print("6. list - List all tasks")
    print("7. list todo - List all tasks that are not done")
    print("8. list in-progress - List all tasks that are in progress")
    print("9. list done - List all completed tasks")
    print("0. exit - Exit the program")
    print("\nChoose an option by typing the corresponding number.")


def main():
    """Fungsi utama untuk menangani input perintah dari pengguna."""
    while True:
        show_menu()
        user_input = input("\nEnter your choice: ").strip()
        
        if user_input == "0":
            print("Exiting Task Tracker CLI. Goodbye!")
            break
        
        # Parsing input
        user_input = user_input.split(" ", 1)
        command = user_input[0].lower()
        
        if command == "add" and len(user_input) > 1:
            description = user_input[1]
            add_task(description)
        
        elif command == "update" and len(user_input) > 1:
            task_id, new_description = user_input[1].split(" ", 1)
            update_task(int(task_id), new_description)
        
        elif command == "delete" and len(user_input) > 1:
            task_id = int(user_input[1])
            delete_task(task_id)
        
        elif command == "mark-in-progress" and len(user_input) > 1:
            task_id = int(user_input[1])
            mark_in_progress(task_id)
        
        elif command == "mark-done" and len(user_input) > 1:
            task_id = int(user_input[1])
            mark_done(task_id)
        
        elif command == "list":
            if len(user_input) > 1:
                status = user_input[1]
                list_tasks(status)
            else:
                list_tasks()
        
        else:
            print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
