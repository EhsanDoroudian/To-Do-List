
import sys
import os
from termcolor import cprint, colored  # For colored terminal output

# Import custom exceptions for specific error cases
from exceptions import (
    UserOptionInputError,        # For invalid menu selections
    TasksInputOutOfRangeError,  # When task number doesn't exist
    ZeroUserInput,             # When user enters 0 as input
    NegetiveInputNumber        # When user enters negative number
)



def get_file_path(filename):
    if getattr(sys, 'frozen', False):  # Running as executable
        return os.path.join(os.path.dirname(sys.executable), filename)
    else:  # Running as script
        return filename

TASKS_LIST = "tasks.txt"
COMPLETED_TASKS_LIST = "completed_tasks.txt"


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
    Allows user to modify the text of an existing task in the task list.
    
    Workflow:
    1. Loads current tasks from file
    2. Displays all tasks with numbering
    3. Prompts user to select a task to edit
    4. Validates the selection
    5. Takes new task text input
    6. Updates and saves the task list
    
    Returns:
        str: Colored status message indicating:
             - Success (green) when task is updated
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
        >>> edit_task_in_tasks_list()
        +1: Buy groceries
        +2: Walk the dog
        [User selects 1, enters "Buy organic groceries"]
        "Task updated successfully." [green]
    """
    # Load current tasks from file and get count
    tasks = load_tasks_list(TASKS_LIST)
    length = len(tasks)

    # Only proceed if tasks exist
    if tasks:
        # Display edit section header
        cprint('\n======== Edit a task ======== \n', color='white', attrs=['bold'])

        # Display all tasks with + prefix for selection
        for index, task in enumerate(tasks, start=1):
            cprint(text=f'+{index}: {task}', color='cyan',attrs=['bold'])

        # Get user input for task to edit
        edit_task_input = input(colored(
            '\nSelect the + number to edit: ', color='white', attrs=['bold'])).strip()  # Remove whitespace

        try:
            # Convert and validate input
            task_index = int(edit_task_input)
            
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

            # Get new task text from user
            new_task_input = input('\nEdit the task: ')
            
            # Update the selected task (adjusting for 0-based index)
            tasks[task_index-1] = new_task_input

            # Save the updated task list
            save_tasks_list(TASKS_LIST, tasks)
            
            return colored("\nTask updated successfully.", color='green',attrs=['bold'])

        # Handle various error cases
        except ValueError:  # Non-integer input
            return colored("\nError: Please enter a positive integer number.", color='red', attrs=['bold'])
        
        except TasksInputOutOfRangeError as e:  # Invalid task number
            text = str(e.message) + str(e.len_tasks_list)
            return colored(f'{text}', color='red', attrs=['bold'])
        
        except NegetiveInputNumber as e:  # Negative number
            return colored(f'\n{e.message}', color='red', attrs=['bold'])
        
        except ZeroUserInput as e:  # Zero entered
            return colored(f'\n{e.message}', color='red', attrs=['bold'])

    else:  # No tasks case
        return colored("\nThe tasks list is empty!", color='red', attrs=['bold'])


def search_task_in_tasks_list():
    """
    Searches for tasks containing a keyword in both active and completed task lists.
    
    Features:
    - Searches case-insensitively (converts both tasks and keyword to lowercase)
    - Distinguishes between active and completed tasks in results
    - Provides immediate feedback when no tasks exist
    - Returns appropriate status messages
    
    Returns:
        str: Colored status message indicating:
             - Success (green) when search completes
             - Warning (red) if no tasks exist
             - Warning (red) if no matches found
    
    Output Format:
        For each match found, displays:
        - "Active task [index]: [task]" (green) or
        - "Completed task [index]: [task]" (green)
    
    Example:
        >>> search_task_in_tasks_list()
        [User enters "groceries"]
        Active task 1: Buy groceries
        Completed task 3: Finish groceries shopping
        "Search completed." [green]
    """
    # Load both active and completed tasks
    tasks = load_tasks_list(TASKS_LIST)
    complete_tasks = load_tasks_list(COMPLETED_TASKS_LIST)

    # Display search header
    cprint('\n======== Search tasks ======== \n', color='white', attrs=['bold'])

    # Get search keyword from user (strip whitespace)
    search_user_input = input(colored('Enter your keyword: ', 'white', attrs=['bold'])).strip().lower()  # Convert to lowercase for case-insensitive search

    # Flag to track if any matches are found
    found = False  

    # Check if both lists are empty
    if not tasks and not complete_tasks:
        return colored("\nNo tasks exist yet.", 'red', attrs=['bold'])

    # Search through active tasks
    for index, task in enumerate(tasks, start=1):    
        if search_user_input in task.lower():  # Case-insensitive comparison
            found = True
            # Display active task match with green highlight
            cprint(text=f'\nActive task {index}: {task}', color='green', attrs=['bold'])
    
    # Search through completed tasks
    for index, complete_task in enumerate(complete_tasks, start=1):
        if search_user_input in complete_task.lower():  # Case-insensitive comparison
            found = True
            # Display completed task match with green highlight
            cprint(text=f'\nCompleted task {index}: {complete_task}', color='green', attrs=['bold'])

    # Handle no matches found
    if not found:
        return colored("\nNo matching tasks found.", color='red', attrs=['bold'])

    # Return success message if search completed (regardless of matches found)
    return colored("\nSearch completed.", color='green', attrs=['bold'])


def clear_all_tasks_in_tasks_list():
    """
    Clears all tasks from the active task list after user confirmation.
    
    Features:
    - Requires explicit user confirmation before deletion
    - Handles both 'y' and 'yes' as affirmative responses
    - Provides appropriate feedback for all outcomes
    - Checks for empty list case
    
    Returns:
        str: Colored status message indicating:
             - Success (green) when tasks are cleared
             - Cancellation (red) when user declines
             - Warning (red) when list is already empty
    
    Side Effects:
        - Potentially modifies tasks.txt file
        - Prints confirmation prompt to stdout
    
    Example:
        >>> clear_all_tasks_in_tasks_list()
        [User enters 'y']
        "All tasks cleared." [green]
    """
    # Load current tasks from file
    tasks = load_tasks_list(TASKS_LIST)

    # Display clear tasks header
    cprint("\n======== Clear all tasks ========\n", 'white', attrs=['bold'])

    # Only proceed if tasks exist
    if tasks:
        # Get confirmation from user (strip whitespace)
        user_input = input(colored("Are you sure (y/n)? ", color='white', attrs=['bold'])).strip().lower()  # Normalize to lowercase

        # Check for affirmative response ('y' or 'yes')
        if user_input in ['y', 'yes']:
            # Clear the task list in memory
            tasks.clear()
            # Save the empty list to file
            save_tasks_list(TASKS_LIST, tasks)
            return colored("\nAll tasks cleared.", color='green',attrs=['bold'])
        
        # Return cancellation message for non-affirmative responses
        return colored("\nOperation cancelled.", color='red', attrs=['bold'])

    else:  # No tasks case
        return colored("\nThe tasks list is empty!", color='red', attrs=['bold'])


def display_complete_task_list():
    """
    Displays all tasks from the completed tasks list with numbering.
    
    Features:
    - Loads and displays completed tasks in a numbered list
    - Uses distinct cyan color for completed tasks
    - Provides appropriate feedback when no completed tasks exist
    - Returns colored status messages
    
    Returns:
        str: Colored status message indicating:
             - Success (green) when tasks are displayed
             - Information (red) when no completed tasks exist
    
    Output Format:
        Each completed task is displayed as:
        [number]. [task text]
        
    Example:
        >>> display_complete_task_list()
        1. Finished project
        2. Paid bills
        "All completed tasks displayed." [green]
    """
    # Load completed tasks from persistent storage
    complete_tasks = load_tasks_list(COMPLETED_TASKS_LIST)
    
    # Display section header for completed tasks
    cprint('\n======== List completed tasks ======== \n', 'white', attrs=['bold'])

    # Check if there are completed tasks to display
    if complete_tasks:
        # Enumerate and display each task with numbering
        for num, task in enumerate(complete_tasks, start=1):
            # Format: "1. Task text" with cyan color for visual distinction
            cprint(f'{num}. {task}\n',  color='cyan',  attrs=['bold'])  

        # Return success confirmation message
        return colored("\nAll completed tasks displayed.", color='green',attrs=['bold'])

    else:
        # Return message when no completed tasks exist
        return colored("No completed tasks yet.", 'red',attrs=['bold'])


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
