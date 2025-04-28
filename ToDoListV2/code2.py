import os  # For file path operations
from termcolor import cprint, colored  # For colored terminal output

# Import custom exceptions for specific error cases
from exceptions import (
    UserOptionInputError,        # For invalid menu selections
    TasksInputOutOfRangeError,  # When task number doesn't exist
    ZeroUserInput,             # When user enters 0 as input
    NegetiveInputNumber        # When user enters negative number
)

# Constants for file paths - using uppercase naming convention
TASKS_LIST = "tasks.txt"  # File to store active/current tasks
COMPLETED_TASKS_LIST = "completed_tasks.txt"  # File to store completed tasks


def load_tasks_list(filename):
    """
    Load tasks from a specified text file.
    
    Reads the file line by line, skipping empty lines and separator lines ('----').
    Creates the file if it doesn't exist.
    
    Args:
        filename (str): Path to the file containing tasks
        
    Returns:
        list: A list of task strings with whitespace stripped
        Returns empty list if file doesn't exist
        
    Example:
        >>> load_tasks_list("tasks.txt")
        ['Buy groceries', 'Finish project']
    """
    tasks = []  # Initialize empty task list
    
    # Check if file exists - return empty list if not
    if not os.path.exists(filename):
        return []
    
    # Open file in read mode (automatically closes when done)
    with open(filename, 'r') as file:
        # Process each line in the file
        for line in file.readlines():
            # Check if line has content after stripping whitespace 
            # and doesn't start with separator '----'
            if line.strip() and not line.startswith('----'):
                # Add the stripped line (without extra whitespace) to tasks list
                tasks.append(line.strip())
    
    # Return the populated tasks list
    return tasks


def save_tasks_list(filename, my_tasks_list):
    """
    Save a list of tasks to a specified file with separators between tasks.
    
    Each task is written followed by a separator line ('----') to allow for
    easy parsing when loading tasks later. This creates a human-readable format
    while maintaining structure for programmatic reading.

    Args:
        filename (str): Path to the file where tasks will be saved
        my_tasks_list (list): List of task strings to be saved
        
    Returns:
        None: This function performs file operations but doesn't return a value
        
    Side Effects:
        - Creates or overwrites the specified file
        - Each task will be followed by a separator line in the output file
        
    Example:
        >>> save_tasks_list("tasks.txt", ["Buy milk", "Pay bills"])
        # Creates file with content:
        # Buy milk
        # ----
        # Pay bills
        # ----
    """
    # Open file in write mode ('w') - this will:
    # - Create the file if it doesn't exist
    # - Overwrite the file if it exists
    with open(filename, 'w') as file:
        # Iterate through each task in the provided list
        for task in my_tasks_list:
            # Write the task text followed by newline
            file.write(f'{task}\n')
            file.write(f'----\n')
            
    # File is automatically closed when exiting the 'with' block

def add_new_task_to_list():
    """
    Prompts the user to input a new task and adds it to the task list.
    
    This function:
    1. Displays an add task header
    2. Prompts the user for task input
    3. Validates the input is not empty
    4. Loads existing tasks
    5. Appends the new task
    6. Saves the updated list
    7. Returns appropriate status messages
    
    Returns:
        str: A colored status message indicating:
             - Success (green) if task was added
             - Error (red) if input was empty
             
    Side Effects:
        - May modify the tasks.txt file by adding a new task
        - Prints to stdout for user interaction
        
    Example:
        >>> add_new_task_to_list()
        [Displays prompt]
        "Buy groceries" [user input]
        "\nYour task has been added successfully." [green output]
    """
    # Display formatted header for the add task section
    cprint('\n ======== Add a new task ======== \n', 'white', attrs=['bold'])
    
    # Prompt user for new task with styled input prompt
    # strip() removes leading/trailing whitespace from input
    add_task_input = input(colored("Add new task: ", 'white', attrs=['bold'])).strip()
    
    # Validate input - return error message if empty
    if not add_task_input:
        return colored('\nYour input was empty!', color='red', attrs=['bold'])

    # Load existing tasks from file (using previously defined function)
    tasks = load_tasks_list(TASKS_LIST)
    
    # Add the new task to the list
    tasks.append(add_task_input)

    # Save the updated task list back to file
    save_tasks_list(TASKS_LIST, tasks)

    # Return success message with green colored text
    return colored("\nYour task has been added successfully.", color='green', attrs=['bold'])


def delete_task_from_tasks_list():
    """
    Displays all tasks and allows user to select one for deletion.
    
    Features:
    - Shows numbered list of current tasks
    - Validates user input with multiple checks
    - Handles various error cases with custom exceptions
    - Provides colored feedback for all outcomes
    
    Returns:
        str: Colored status message indicating:
             - Success (green) when task is deleted
             - Error (red) for invalid cases:
               * Empty task list
               * Non-numeric input
               * Out of range numbers
               * Zero/negative numbers
    
    Raises:
        ZeroUserInput: If user enters 0
        NegetiveInputNumber: If user enters negative number
        TasksInputOutOfRangeError: If number exceeds task count
    
    Example:
        >>> delete_task_from_tasks_list()
        *1: Buy groceries
        *2: Do laundry
        [User enters 2]
        "Task number 2 has been deleted" [green]
    """
    # Display delete task section header
    cprint('\n ======== Delete a task ======== \n', 'white', attrs=['bold'])
    
    # Load current tasks and get count
    tasks = load_tasks_list(TASKS_LIST)
    length = len(tasks)

    # Only proceed if tasks exist
    if tasks:
        # Display all tasks with numbered prefixes
        for index, task in enumerate(tasks, start=1):
            cprint(text=f'*{index}: {task}', color='cyan', attrs=['bold'])

        try:
            # Get and validate user selection
            delete_task_input = int(input(colored('\nSelect the * number to delete the task: ',color='white',attrs=['bold'])).strip())
            
            # Custom exception cases
            if delete_task_input == 0:
                raise ZeroUserInput(message='There is no Zero number in your list.')

            elif delete_task_input < 0:
                raise NegetiveInputNumber(message='Please enter positive number.')

            elif delete_task_input not in range(1, length+1):
                raise TasksInputOutOfRangeError(
                    message='\nError: The number is not in the list. The last number in the list is: ',
                    len_tasks_list=length
                )
            
        # Handle various error cases
        except ValueError:  # Non-integer input
            return colored('\nInvalid input. Please enter a number.', color='red', attrs=['bold'])

        except TasksInputOutOfRangeError as e:  # Number too high
            text = str(e.message) + str(e.len_tasks_list)
            return colored(f'\n{text}', color='red', attrs=['bold'])

        except NegetiveInputNumber as e:  # Negative number
            return colored(f'\n{e.message}', color='red', attrs=['bold'])

        except ZeroUserInput as e:  # Zero entered
            return colored(f'\n{e.message}', color='red', attrs=['bold'])

        # If validation passed, delete the task
        del tasks[delete_task_input-1]  # Adjust for 0-based index
        save_tasks_list(TASKS_LIST, tasks)  # Persist changes

        return colored(f"\nTask number {delete_task_input} has been deleted", 
                      color='green', attrs=['bold'])

    else:  # No tasks case
        return colored("\nThe tasks list is empty!", color='red', attrs=['bold'])


def display_tasks_list():
    """
    Displays all tasks from the active task list with numbering.
    
    This function:
    - Loads the current tasks from persistent storage
    - Shows them in a formatted numbered list if tasks exist
    - Provides appropriate feedback when no tasks exist
    - Uses consistent styling for all output messages
    
    Returns:
        str: A colored message indicating:
             - Success (green) when tasks are displayed
             - Warning (red) when task list is empty
             
    Output Format:
        Each task is displayed in the format:
        [index]. [task description]
        
    Example:
        >>> display_tasks_list()
        1. Buy groceries
        2. Walk the dog
        "All tasks displayed." [green]
        
        OR if empty:
        "The tasks list is empty!" [red]
    """
    # Load current tasks from file using helper function
    tasks = load_tasks_list(TASKS_LIST)

    # Check if tasks exist
    if tasks:
        # Display section header with consistent formatting
        cprint('\n======== List tasks ======== \n', color='white', attrs=['bold'])
        
        # Enumerate and display each task with numbering
        for index, task in enumerate(tasks, start=1):
            # Format: "1. Task description" with newline
            cprint(f'{index}. {task}\n', 
                  color='white',  # Consistent text color 
                  attrs=['bold']) # Bold for better readability
        
        # Return success confirmation message
        return colored("All tasks displayed.", 
                      color='green',  # Success color
                      attrs=['bold'])

    else:
        # Return empty list warning message
        return colored("\nThe tasks list is empty!", 
                      color='red',  # Warning color
                      attrs=['bold'])


def mark_task_as_complete_task():
    """
    Allows user to move a task from the active list to the completed list.
    
    Functionality:
    - Displays all active tasks with numbering
    - Prompts user to select a task to complete
    - Validates the user input
    - Moves selected task to completed list
    - Updates both task files
    - Provides colored feedback
    
    Returns:
        str: Colored status message indicating:
             - Success (green) when task is completed
             - Error (red) for invalid cases:
               * Empty task list
               * Non-numeric input
               * Out of range numbers
               * Zero/negative numbers
    
    Raises:
        ZeroUserInput: If user enters 0
        NegetiveInputNumber: If user enters negative number
        TasksInputOutOfRangeError: If number exceeds task count
    
    Side Effects:
        - Modifies both tasks.txt and completed_tasks.txt files
        - Prints to stdout for user interaction
    
    Example:
        >>> mark_task_as_complete_task()
        +1: Buy groceries
        +2: Walk the dog
        [User enters 1]
        "Task marked as completed." [green]
    """
    # Load current tasks and completed tasks
    tasks = load_tasks_list(TASKS_LIST)
    length = len(tasks)  # Get count of active tasks
    complete_tasks = load_tasks_list(COMPLETED_TASKS_LIST)

    # Only proceed if there are tasks to complete
    if tasks:
        # Display completion section header
        cprint('\n======== Mark task as completed ======== \n', color='white', attrs=['bold'])
        
        # Show all tasks with + prefix for selection
        for index, task in enumerate(tasks, start=1):
            cprint(text=f'+{index}: {task}', 
                  color='cyan',  # Distinct color for selection
                  attrs=['bold'])

        # Get user input for task to complete
        complete_task_input = input(colored(
            '\nSelect the + number to mark as completed: ', color='white',attrs=['bold'])).strip()  # Remove whitespace

        try:
            # Convert and validate input
            task_index = int(complete_task_input)
            
            # Custom validation checks
            if task_index == 0:
                raise ZeroUserInput(message='There is no Zero number in your list.')
            
            elif task_index < 0:
                raise NegetiveInputNumber(message='Please enter positive number.')
            
            elif task_index not in range(1, length+1):
                raise TasksInputOutOfRangeError(
                    message="\nError: The number is not in the list. The last number in the list is: ",
                    len_tasks_list=length,
                ) 
            
            # Move task from active to completed
            complete_tasks.append(tasks[task_index-1])  # Add to completed
            del tasks[task_index-1]  # Remove from active

            # Persist changes to both files
            save_tasks_list(TASKS_LIST, tasks)
            save_tasks_list(COMPLETED_TASKS_LIST, complete_tasks)

            return colored("\nTask marked as completed.", 
                         color='green',  # Success color
                         attrs=['bold'])
        
        # Handle various error cases
        except ValueError:  # Non-integer input
            return colored("\nError: Please enter a number.", color='red', attrs=['bold'])
        
        except TasksInputOutOfRangeError as e:  # Invalid task number
            text = str(e.message) + str(e.len_tasks_list)
            return colored(f'{text}', color='red', attrs=['bold'])
        
        except NegetiveInputNumber as e:  # Negative number
            return colored(f'\n{e.message}', color='red', attrs=['bold'])
        
        except ZeroUserInput as e:  # Zero entered
            return colored(f'\n{e.message}', color='red', attrs=['bold'])

    else:  # No tasks case
        return colored("\nThe tasks list is empty!", color='red', attrs=['bold'])

def edit_task_in_tasks_list():
    """
    Allow the user to edit the content of an existing task.
    """
    tasks = load_tasks_list(TASKS_LIST)
    length = len(tasks)
    if tasks:
        cprint('\n======== Edit a task ======== \n', color='white', attrs=['bold'])

        for index, task in enumerate(tasks, start=1):
            cprint(text=f'+{index}: {task}', color='cyan', attrs=['bold'])

        edit_task_input = input(colored('\nSelect the + number to edit: ', color='white', attrs=['bold'])).strip()

        try:
            task_index = int(edit_task_input)
            if task_index == 0:
                raise ZeroUserInput(message='There is no Zero number in your list.')

            elif task_index < 0:
                raise NegetiveInputNumber(message='Please enter positive number.')

            elif task_index not in range(1, length+1):
                raise TasksInputOutOfRangeError(
                    message="\nError: The number is not in the list. The last number in the list is: ",
                    len_tasks_list=length,
                    ) 

            new_task_input = input('\nEdit the task: ')
            tasks[task_index-1] = new_task_input

            save_tasks_list(TASKS_LIST, tasks)
            
            return colored("\nTask updated successfully.", color='green', attrs=['bold'])

        except ValueError:
            return colored("\nError: Please enter a positive integer number.", color='red', attrs=['bold'])

        except TasksInputOutOfRangeError as e:
            text = str(e.message) + str(e.len_tasks_list)
            return colored(f'{text}', color='red', attrs=['bold'])

        except NegetiveInputNumber as e:
            return colored(f'\n{e.message}', color='red', attrs=['bold'])
        
        except ZeroUserInput as e:
            return colored(f'\n{e.message}', color='red', attrs=['bold'])

    else:
        return colored(f"\nThe tasks list is empty!", color='red', attrs=['bold'])
    

def search_task_in_tasks_list():
    """
    Search for tasks by keyword in both active and completed lists.
    """
    tasks = load_tasks_list(TASKS_LIST)
    complete_tasks = load_tasks_list(COMPLETED_TASKS_LIST)

    cprint('\n======== Search tasks ======== \n', color='white', attrs=['bold'])

    search_user_input = input(colored('Enter your keyword: ', 'white', attrs=['bold'])).strip()

    found = False  # Flag to track if any matches found

    if not tasks and not complete_tasks:
        return colored("\nNo tasks exist yet.", 'red', attrs=['bold'])

    for index, task in enumerate(tasks, start=1):    
        if search_user_input in task.lower():
            found = True
            cprint(text=f'\nActive task {index}: {task}', color='green', attrs=['bold'])
    
    for index, complete_task in enumerate(complete_tasks, start=1):
        if search_user_input in complete_task.lower():
            found = True
            cprint(text=f'\nCompleted task {index}: {complete_task}', color='green', attrs=['bold'])

    if not found:
        return colored("\nNo matching tasks found.", color='red', attrs=['bold'])

    return colored("\nSearch completed.", color='green', attrs=['bold'])


def clear_all_tasks_in_tasks_list():
    """
    Clear all tasks in the active list after confirmation from the user.
    """
    tasks = load_tasks_list(TASKS_LIST)

    cprint("\n======== Clear all tasks ========\n", 'white', attrs=['bold'])

    if tasks:
        user_input = input(colored("Are you sure (y/n)? ", color='white', attrs=['bold'])).strip()
        if user_input.lower() in ['y', 'yes']:
            tasks.clear()
            save_tasks_list(TASKS_LIST, tasks)
            return colored("\nAll tasks cleared.", color='green', attrs=['bold'])
        
        return colored("\nOperation cancelled.", color='red', attrs=['bold'])

    else:
        return colored(f"\nThe tasks list is empty!", color='red', attrs=['bold'])


def display_complete_task_list():
    """
    Display all completed tasks.
    """
    complete_tasks = load_tasks_list(COMPLETED_TASKS_LIST)
    cprint('\n======== List completed tasks ======== \n', 'white', attrs=['bold'])

    if complete_tasks:
        for num, task in enumerate(complete_tasks, start=1):
            cprint(f'{num}. {task}\n',  color='cyan', attrs=['bold'])

        return colored("\nAll completed tasks displayed.", color='green', attrs=['bold'])

    else:
        return colored("No completed tasks yet.", 'red', attrs=['bold'])


# Main execution block
if __name__ == "__main__":
    # Ensure both task files exist
    for file in [TASKS_LIST, COMPLETED_TASKS_LIST]:
        if not os.path.exists(file):
            open(file=file, mode='w').close()

    while True:
        # Display menu options
        print(colored("\nTask Manager Menu", color='white', attrs=['bold']))
        print("-----------------")
        print(colored(text="1. Add a new task", color='blue', attrs=['bold']))
        print(colored(text="2. Delete a task", color='blue', attrs=['bold']))
        print(colored(text="3. List tasks", color='blue', attrs=['bold']))
        print(colored(text="4. Mark task as completed", color='blue', attrs=['bold']))
        print(colored(text='5. Edit a task', color='blue', attrs=['bold']))
        print(colored(text='6. Search tasks', color='blue', attrs=['bold']))
        print(colored(text='7. Clear all tasks', color='blue', attrs=['bold']))
        print(colored(text='8. List completed tasks', color='blue', attrs=['bold']))
        print(colored(text='9. Quit', color='red', attrs=['bold']))
    
        user_option_input = input(colored("\nEnter your choice(1-9): ", 'white', attrs=['bold'])).strip()

        if user_option_input.lower() in ['q', 'quit', 'exit']:
            cprint("\nGoodBye👋", color='magenta',attrs=['bold'])
            break

        try:
            user_option_input = int(user_option_input)
            if user_option_input not in range(1, 10):
                raise UserOptionInputError(
                    message="\nInvalid input. Please enter a number between 1-9. Your input was ",
                    num_input=user_option_input,
                )
            
        except ValueError:
            cprint('\nInvalid input. Please enter a number.', color='red', attrs=['bold'])

        except UserOptionInputError as e:
            text = str(e.message) + str(e.num_input)
            cprint(text=text, color='red', attrs=['bold'])

        # Match user input to corresponding function
        match user_option_input:
            case 1:
                print(add_new_task_to_list())
            case 2:
                print(delete_task_from_tasks_list())
            case 3:
                print(display_tasks_list())
            case 4:
                print(mark_task_as_complete_task())
            case 5:
                print(edit_task_in_tasks_list())
            case 6:
                print(search_task_in_tasks_list())
            case 7:
                print(clear_all_tasks_in_tasks_list())
            case 8:
                print(display_complete_task_list())
            case 9:
                cprint("\nGoodBye👋", color='magenta',attrs=['bold'])
                break
