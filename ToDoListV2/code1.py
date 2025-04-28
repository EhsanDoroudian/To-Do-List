"""
Task Management System
A simple command-line program to manage tasks (to-do items)
Features: Add, delete, edit, complete, search, and clear tasks
"""

# List to store active/incomplete tasks
tasks = []

# List to store completed tasks
complete_tasks = []


def add_new_task_to_list():
    """
    Adds a new task entered by the user to the tasks list.
    Steps:
    1. Show header
    2. Get user input
    3. Add to tasks list
    4. Return confirmation
    """
    print('\n ======== Add a new task ======== \n'.title())
    add_task_input = input("Add new task: ")
    tasks.append(add_task_input)  # Add task to the list

    return "Your task has been added successfully."


def delete_task_from_tasks_list():
    """
    Deletes a selected task from the list.
    Steps:
    1. Check if tasks exist
    2. Display numbered tasks
    3. Get user selection
    4. Validate input
    5. Delete task
    6. Return confirmation
    """
    if tasks:
        print('\n ======== Delete a task ======== \n'.upper())
        
        # Display tasks with 1-based numbering
        for index, task in enumerate(tasks):
            print(f'*{index+1}: {task}')

        delete_task_input = input('Select the * number to delete the task: ')

        # Input validation
        if not delete_task_input.isnumeric():
            return "\nError: Please enter a positive integer number."
        
        task_index = int(delete_task_input)
        
        # Check if number is in valid range
        if task_index not in range(1, len(tasks)+1):
            return "\nError: The number is not in the list."

        # Delete the task (adjusting for 0-based index)
        del tasks[task_index-1]

        return f"\nTask number {delete_task_input} has been deleted"
    
    else:
        return "\nThe tasks list is empty!"


def display_tasks_list():
    """
    Displays all current tasks with numbering.
    Handles empty list case.
    """
    if tasks:
        print('\n======== List tasks ======== \n'.lower())
        for num, task in enumerate(tasks, start=1):
            print(f'{num}. {task}\n')
        
        return "All tasks displayed."

    else:
        return "The tasks list is empty!"


def mark_task_as_complete_task():
    """
    Marks a task as complete and moves it to completed list.
    Steps:
    1. Check for tasks
    2. Display numbered tasks
    3. Get user selection
    4. Validate input
    5. Move task to completed
    6. Return confirmation
    """
    if tasks:
        print('\n======== Mark task as completed ======== \n'.capitalize())

        # Display tasks with numbering
        for index, task in enumerate(tasks, start=1):
            print(f'+{index}: {task}')

        complete_task_input = input('Select the + number to mark as completed: ')

        # Input validation
        if not complete_task_input.isnumeric():
            return "\nError: Please enter a positive integer number."
        
        task_index = int(complete_task_input)
        
        if task_index not in range(1, len(tasks)+1):
            return "\nError: The number is not in the list."
        
        # Move task to completed list and remove from active
        complete_tasks.append(tasks[task_index-1])
        del tasks[task_index-1]

        return "\nTask marked as completed."

    else:
        return "The tasks list is empty!"


def edit_task_in_tasks_list():
    """
    Edits an existing task.
    Steps:
    1. Check for tasks
    2. Display numbered tasks
    3. Get selection
    4. Validate input
    5. Get new task text
    6. Update task
    """
    if tasks:
        print('\n======== Edit a task ======== \n'.title())

        # Display tasks with edit markers
        for index, task in enumerate(tasks, start=1):
            print(f'#{index}: {task}')

        edit_task_input = input('Select the # number to edit: ')

        # Input validation
        if not edit_task_input.isnumeric():
            return "\nError: Please enter a positive integer number."

        task_index = int(edit_task_input)
        
        if task_index not in range(1, len(tasks)+1):
            return "\nError: The number is not in the list."

        # Get and update task text
        new_task_input = input('\nEdit the task: ')
        tasks[task_index-1] = new_task_input
        
        return "\nTask updated successfully."
    
    else:
        return "\nThe tasks list is empty!"


def search_task_in_tasks_list():
    """
    Searches for tasks containing a keyword in both active and completed lists.
    Returns matching tasks with their status.
    """
    print('\n======== Search tasks ======== \n'.title())

    search_user_input = input('Enter your keyword: ').lower()

    found = False  # Flag to track if any matches found

    # Check both lists
    if not tasks and not complete_tasks:
        return "\nNo tasks exist yet."

    # Search active tasks
    for index, task in enumerate(tasks, start=1):    
        if search_user_input in task.lower():
            found = True
            print(f'Active task {index}: {task}')
    
    # Search completed tasks
    for index, complete_task in enumerate(complete_tasks, start=1):
        if search_user_input in complete_task.lower():
            found = True
            print(f'Completed task {index}: {complete_task}')

    if not found:
        return "\nNo matching tasks found."

    return "\nSearch completed."


def clear_all_tasks_in_tasks_list():
    """
    Clears all tasks after confirmation.
    Safety measure to prevent accidental deletion.
    """
    print("\n======== Clear all tasks ========\n".title())

    if tasks:
        # Confirm before clearing
        user_input = input("Are you sure (y/n)? ").lower()
        if user_input in ['y', 'yes']:
            tasks.clear()
            return "\nAll tasks cleared."
        
        return "\nOperation cancelled."

    else:
        return "The tasks list is already empty."


def display_complete_task_list():
    """
    Displays all completed tasks with numbering.
    """
    print('\n======== List completed tasks ======== \n'.title())

    if complete_tasks:
        for num, task in enumerate(complete_tasks, start=1):
            print(f'{num}. {task}\n')

        return "All completed tasks displayed."

    else:
        return "No completed tasks yet."


# Main program execution
if __name__ == "__main__":
    while True:
        # Display menu options
        print("\nTask Manager Menu")
        print("-----------------")
        print("1. Add a new task")
        print("2. Delete a task")
        print("3. List tasks")
        print("4. Mark task as completed")
        print("5. Edit a task")
        print("6. Search tasks")
        print("7. Clear all tasks")
        print("8. List completed tasks")
        print("9. Quit")

        user_input = input("Enter your choice (1-9): ")

        # Input validation
        if user_input.isnumeric():
            if int(user_input) == 0 or int(user_input) >= 10:
                print('\nInvalid input. Please enter a number between 1-9.')

        else:
            if user_input.lower() in ['q', 'quit', 'exit']:
                break
            print('\nInvalid input. Please enter a number.')

        # Process user selection
        match user_input:
            case '1':
                print(add_new_task_to_list())
            case '2':
                print(delete_task_from_tasks_list())
            case '3':
                print(display_tasks_list())
            case '4':
                print(mark_task_as_complete_task())
            case '5':
                print(edit_task_in_tasks_list())
            case '6':
                print(search_task_in_tasks_list())
            case '7':
                print(clear_all_tasks_in_tasks_list())
            case '8':
                print(display_complete_task_list())
            case '9':
                print("Goodbye!")
                break  # Exit program
        