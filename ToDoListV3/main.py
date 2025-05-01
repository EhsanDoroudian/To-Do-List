import os
import datetime
import colorama
from colorama import Fore, Style

from exceptions import UserOptionInputError, TasksInputOutOfRangeError, NegetiveInputNumber, ZeroUserInput


class ToDoList:

    colorama.init()
    bold = Style.BRIGHT
    white = Fore.WHITE + bold
    red = Fore.RED + bold
    green = Fore.GREEN + bold
    magenta = Fore.MAGENTA + bold
    cyan = Fore.CYAN + bold

    def __init__(self, tasks_file="tasks.txt", completed_tasks_file="complete_tasks.txt"):
        self._TASKS_FILE = tasks_file
        self._COMPLETE_TASKS_FILE = completed_tasks_file
        self._tasks = []
        self._complete_list = []
        self._create_date = datetime.datetime.now()
        self._length = 0

    def _load_tasks_file(self, filename):
        tasks_list = []
        if not os.path.exists(filename):
            return []
        
        with open(filename, 'r') as file:
            tasks_list = [line.strip() for line in file.readlines() if line.strip() and not line.startswith('----')]
        return tasks_list
    
    def _save_tasks_file(self, filename, tasks_list):
        with open(filename, 'w') as file:
            for task in tasks_list:
                file.write(f'{task}\n')
                file.write('----\n')
    
    def _add_task_to_tasks_file(self):
        print(self.white + '\n ======== Add a new task ======== \n')
        
        add_task_input = input(self.white + "Add new task: ").strip()
        
        if not add_task_input:
            return self.red + '\nYour input was empty!'

        tasks = self._load_tasks_file(self._TASKS_FILE)
        
        tasks.append(add_task_input)

        self._save_tasks_file(self._TASKS_FILE, tasks)

        return self.green + "\nYour task has been added successfully."
    
    def _delete_task_from_tasks_list(self):
        # Display delete task section header
        print(self.white + '\n ======== Delete a task ======== \n')
        
        # Load current tasks and get count
        tasks = self._load_tasks_file(self._TASKS_FILE)
        length = len(tasks)

        # Only proceed if tasks exist
        if tasks:
            # Display all tasks with numbered prefixes
            for index, task in enumerate(tasks, start=1):
                print(self.cyan + f'*{index}: {task}')

            try:
                # Get and validate user selection
                delete_task_input = int(input(self.white + '\nSelect the * number to delete the task: ').strip())
                
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
                return self.red + '\nInvalid input. Please enter a number.'

            except TasksInputOutOfRangeError as e:  # Number too high
                text = str(e.message) + str(e.len_tasks_list)
                return self.red + f'\n{text}'

            except NegetiveInputNumber as e:  # Negative number
                return self.red + f'\n{e.message}'

            except ZeroUserInput as e:  # Zero entered
                return self.red + f'\n{e.message}'

            # If validation passed, delete the task
            del tasks[delete_task_input-1]  # Adjust for 0-based index
            self._save_tasks_file(self._TASKS_FILE, tasks)  # Persist changes

            return self.green + f"\nTask number {delete_task_input} has been deleted"
        
        else:  # No tasks case
            return self.red + "\nThe tasks list is empty!"

    def _display_tasks_list(self):
        # Load current tasks from file using helper function
        tasks = self._load_tasks_file(self._TASKS_FILE)

        # Check if tasks exist
        if tasks:
            # Display section header with consistent formatting
            print(self.white + '\n======== List tasks ======== \n')
            
            # Enumerate and display each task with numbering
            for index, task in enumerate(tasks, start=1):
                # Format: "1. Task description" with newline
                print(self.white + f'{index}. {task}\n')
            
            # Return success confirmation message
            return self.green + "All tasks displayed.", 

        else:
            # Return empty list warning message
            return self.red + "\nThe tasks list is empty!", 

    def _mark_task_as_complete_task(self):
        # Load current tasks and completed tasks
        tasks = self._load_tasks_file(self._TASKS_FILE)
        length = len(tasks)  # Get count of active tasks
        complete_tasks = self._load_tasks_file(self._COMPLETE_TASKS_FILE)

        # Only proceed if there are tasks to complete
        if tasks:
            # Display completion section header
            print(self.white + '\n======== Mark task as completed ======== \n')

            # Show all tasks with + prefix for selection
            for index, task in enumerate(tasks, start=1):
                print(self.cyan + f'+{index}: {task}')

            # Get user input for task to complete
            complete_task_input = input(self.white + '\nSelect the + number to mark as completed: ').strip()  # Remove whitespace

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
                self._save_tasks_file(self._TASKS_FILE, tasks)
                self._save_tasks_file(self._COMPLETE_TASKS_FILE, complete_tasks)

                return self.green + "\nTask marked as completed."

            # Handle various error cases
            except ValueError:  # Non-integer input
                return self.red + "\nError: Please enter a number."

            except TasksInputOutOfRangeError as e:  # Invalid task number
                text = str(e.message) + str(e.len_tasks_list)
                return self.red + f'{text}'

            except NegetiveInputNumber as e:  # Negative number
                return self.red + f'\n{e.message}'

            except ZeroUserInput as e:  # Zero entered
                return self.red + f'\n{e.message}'

        else:  # No tasks case
            return self.red + "\nThe tasks list is empty!"
    
    def _edit_task_in_tasks_list(self):
        # Load current tasks from file and get count
        tasks = self._load_tasks_file(self._TASKS_FILE)
        self._length = len(tasks)

        # Only proceed if tasks exist
        if tasks:
            # Display edit section header
            print(self.white + '\n======== Edit a task ======== \n')

            # Display all tasks with + prefix for selection
            for index, task in enumerate(tasks, start=1):
                print(self.cyan + f'+{index}: {task}')

            # Get user input for task to edit
            edit_task_input = input(self.white + '\nSelect the + number to edit: ').strip()  # Remove whitespace

            try:
                # Convert and validate input
                task_index = int(edit_task_input)
                
                # Custom validation checks
                if task_index == 0:
                    raise ZeroUserInput(message='There is no Zero number in your list.')
                elif task_index < 0:
                    raise NegetiveInputNumber(message='Please enter positive number.')
                
                elif task_index not in range(1, self._length+1):
                    raise TasksInputOutOfRangeError(
                        message="\nError: The number is not in the list. The last number in the list is: ",
                        len_tasks_list=self._length,
                    )

                # Get new task text from user
                new_task_input = input('\nEdit the task: ')
                
                # Update the selected task (adjusting for 0-based index)
                tasks[task_index-1] = new_task_input

                # Save the updated task list
                self._save_tasks_file(self._TASKS_FILE, tasks)
                
                return self.green + "\nTask updated successfully."

            # Handle various error cases
            except ValueError:  # Non-integer input
                return self.red + "\nError: Please enter a positive integer number."
            
            except TasksInputOutOfRangeError as e:  # Invalid task number
                text = str(e.message) + str(e.len_tasks_list)
                return self.red + f'{text}'
            
            except NegetiveInputNumber as e:  # Negative number
                return self.red + f'\n{e.message}'
            
            except ZeroUserInput as e:  # Zero entered
                return self.red + f'\n{e.message}'

        else:  # No tasks case
            return self.red + "\nThe tasks list is empty!"
         
    def _search_task_in_tasks_list(self):
        # Load both active and completed tasks
        tasks = self._load_tasks_file(self._TASKS_FILE)
        complete_tasks = self._load_tasks_file(self._COMPLETE_TASKS_FILE)

        # Display search header
        print(self.white + '\n======== Search tasks ======== \n')

        # Get search keyword from user (strip whitespace)
        search_user_input = input(self.white + 'Enter your keyword: ').strip().lower()  # Convert to lowercase for case-insensitive search

        # Flag to track if any matches are found
        found = False  

        # Check if both lists are empty
        if not tasks and not complete_tasks:
            return self.red + "\nNo tasks exist yet."

        # Search through active tasks
        for index, task in enumerate(tasks, start=1):    
            if search_user_input in task.lower():  # Case-insensitive comparison
                found = True
                # Display active task match with green highlight
                print(self.green + f'\nActive task {index}: {task}')
        
        # Search through completed tasks
        for index, complete_task in enumerate(complete_tasks, start=1):
            if search_user_input in complete_task.lower():  # Case-insensitive comparison
                found = True
                # Display completed task match with green highlight
                print(self.green + f'\nCompleted task {index}: {complete_task}')

        # Handle no matches found
        if not found:
            return self.red + "\nNo matching tasks found."

        # Return success message if search completed (regardless of matches found)
        return self.green + "\nSearch completed."
    
    def _clear_all_tasks_in_tasks_list(self):
        # Load current tasks from file
        tasks = self._load_tasks_file(self._TASKS_FILE)

        # Display clear tasks header
        print(self.white + "\n======== Clear all tasks ========\n")

        # Only proceed if tasks exist
        if tasks:
            # Get confirmation from user (strip whitespace)
            user_input = input(self.white + "Are you sure (y/n)? ").strip().lower()  # Normalize to lowercase

            # Check for affirmative response ('y' or 'yes')
            if user_input in ['y', 'yes']:
                # Clear the task list in memory
                tasks.clear()
                # Save the empty list to file
                self._save_tasks_file(self._TASKS_FILE, tasks)
                return self.green + "\nAll tasks cleared."
            
            # Return cancellation message for non-affirmative responses
            return self.red + "\nOperation cancelled."

        else:  # No tasks case
            return self.red + "\nThe tasks list is empty!"
    
    def _display_complete_task_list(self):
        # Load completed tasks from persistent storage
        complete_tasks = self._load_tasks_file(self._COMPLETE_TASKS_FILE)
        
        # Display section header for completed tasks
        print(self.white + '\n======== List completed tasks ======== \n')

        # Check if there are completed tasks to display
        if complete_tasks:
            # Enumerate and display each task with numbering
            for num, task in enumerate(complete_tasks, start=1):
                # Format: "1. Task text" with cyan color for visual distinction
                print(self.cyan + f'{num}. {task}\n')  

            # Return success confirmation message
            return self.green + "\nAll completed tasks displayed."

        else:
            # Return message when no completed tasks exist
            return self.red + "No completed tasks yet."

    def start(self):
        for file in [self._TASKS_FILE, self._COMPLETE_TASKS_FILE]:
            if not os.path.exists(file):
                open(file=file, mode='w').close()

        while True:
            # Display menu options
            print(self.white + "\nTask Manager Menu")
            print(self.white + "-----------------")
            print(self.white + "1. Add a new task")
            print(self.white + "2. Delete a task")
            print(self.white + "3. List tasks")
            print(self.white + "4. Mark task as completed")
            print(self.white + "5. Edit a task")
            print(self.white + "6. Search tasks")
            print(self.white + "7. Clear all tasks")
            print(self.white + "8. List completed tasks")
            print(self.white + "9. Quit")

            user_option_input = input(self.white + "\nEnter your choice(1-9): ").strip()

            if user_option_input.lower() in ['q', 'quit', 'exit']:
                print(self.magenta + "\nGoodBye👋")
                break

            try:
                user_option_input = int(user_option_input)
                if user_option_input not in range(1, 10):
                    raise UserOptionInputError(
                        message="\nInvalid input. Please enter a number between 1-9. Your input was ",
                        num_input=user_option_input,
                    )
                
            except ValueError:
                print(self.bold + self.red +'\nInvalid input. Please enter a number.')

            except UserOptionInputError as e:
                text = str(e.message) + str(e.num_input)
                print(self.bold + self.red  + text)


            # Match user input to corresponding function
            match user_option_input:
                case 1:
                    print(self._add_task_to_tasks_file())
                case 2:
                    print(self._delete_task_from_tasks_list())
                case 3:
                    print(self._display_tasks_list())
                case 4:
                    print(self._mark_task_as_complete_task())
                case 5:
                    print(self._edit_task_in_tasks_list())
                case 6:
                    print(self._search_task_in_tasks_list())
                case 7:
                    print(self._clear_all_tasks_in_tasks_list())
                case 8:
                    print(self._display_complete_task_list())
                case 9:
                    print(self.magenta + "\nGoodBye👋")
                    break

if __name__ == "__main__":
    app = ToDoList()
    app.start()