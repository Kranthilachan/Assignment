import sqlite3

# Connect to SQLite database
try:
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Database connection error: {e}")
    exit(1)

# Check table structure
try:
    cursor.execute("PRAGMA table_info(tasks)")
    columns = cursor.fetchall()
    for column in columns:
        print(column)
except sqlite3.Error as e:
    print(f"Error fetching table info: {e}")

# Drop and recreate table with `deadline` column
try:
    cursor.execute("DROP TABLE IF EXISTS tasks")
    conn.commit()

    cursor.execute("""
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        deadline TEXT,
        status TEXT CHECK(status IN ('pending', 'completed')) NOT NULL DEFAULT 'pending'
    )
    """)
    conn.commit()
except sqlite3.Error as e:
    print(f"Error creating table: {e}")

# CRUD Operations

# Function to add a new task
def add_task():
    try:
        description = input("Enter task description: ").strip()
        if not description:
            print("Task description cannot be empty.")
            return
        
        deadline = input("Enter deadline (YYYY-MM-DD) [optional]: ").strip().strip('"') or None

        cursor.execute("INSERT INTO tasks (description, deadline) VALUES (?, ?)", (description, deadline))
        conn.commit()
        print("Task added successfully!")
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")

# Function to view all tasks
def view_all_tasks():
    try:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        if not tasks:
            print("No tasks found.")
            return
        
        print("\nAll Tasks:")
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2] or 'N/A'}, Status: {task[3]}")
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")

# Function to view pending tasks
def view_pending_tasks():
    try:
        cursor.execute("SELECT * FROM tasks WHERE status='pending'")
        tasks = cursor.fetchall()
        if not tasks:
            print("No pending tasks.")
            return
        
        print("\nPending Tasks:")
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2] or 'N/A'}")
    except sqlite3.Error as e:
        print(f"Error fetching pending tasks: {e}")

# Function to view completed tasks
def view_completed_tasks():
    try:
        cursor.execute("SELECT * FROM tasks WHERE status='completed'")
        tasks = cursor.fetchall()
        if not tasks:
            print("No completed tasks.")
            return
        
        print("\nCompleted Tasks:")
        for task in tasks:
            print(f"ID: {task[0]}, Description: {task[1]}, Deadline: {task[2] or 'N/A'}")
    except sqlite3.Error as e:
        print(f"Error fetching completed tasks: {e}")

# Function to update a task
def update_task():
    try:
        task_id = input("Enter task ID to update: ").strip()
        cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task = cursor.fetchone()
        
        if not task:
            print("Task not found.")
            return

        new_desc = input(f"Enter new description [{task[1]}]: ").strip() or task[1]
        new_deadline = input(f"Enter new deadline (YYYY-MM-DD) [{task[2] or 'N/A'}]: ").strip() or task[2]
        new_status = input("Enter new status (pending/completed): ").strip().lower()

        if new_status not in ["pending", "completed"]:
            print("Invalid status! Task not updated.")
            return

        cursor.execute("UPDATE tasks SET description=?, deadline=?, status=? WHERE id=?", 
                       (new_desc, new_deadline, new_status, task_id))
        conn.commit()
        print("Task updated successfully!")
    except sqlite3.Error as e:
        print(f"Error updating task: {e}")

# Function to delete a task
def delete_task():
    try:
        task_id = input("Enter task ID to delete: ").strip()
        cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task = cursor.fetchone()

        if not task:
            print("Task not found.")
            return

        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        print("Task deleted successfully!")
    except sqlite3.Error as e:
        print(f"Error deleting task: {e}")

# User Interface
def main():
    while True:
        print("\nTask Manager Menu")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update a task")
        print("6. Delete a task")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            view_all_tasks()
        elif choice == "3":
            view_pending_tasks()
        elif choice == "4":
            view_completed_tasks()
        elif choice == "5":
            update_task()
        elif choice == "6":
            delete_task()
        elif choice == "7":
            print("Exiting...")
            conn.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
