import csv
import os
import datetime
import colorama
from colorama import Fore, Style

from exceptions import UserOptionInputError, TasksInputOutOfRangeError, NegetiveInputNumber, ZeroUserInput


class ToDoList:
    colorama.init()  # Initialize colorama
    bold = Style.BRIGHT
    white = Fore.WHITE + bold
    red = Fore.RED + bold
    green = Fore.GREEN + bold
    magenta = Fore.MAGENTA + bold
    cyan = Fore.CYAN + bold

    def __init__(self, tasks_file="tasks.csv", completed_tasks_file="complete_tasks.csv"):
        self._TASKS_FILE = tasks_file
        self._COMPLETE_TASKS_FILE = completed_tasks_file
        self._tasks = []
        self._complete_list = []
        self._create_date = datetime.datetime.now()
        self._length = 0
        
        # Initialize CSV files with headers if they don't exist
        if not os.path.exists(self._TASKS_FILE):
            with open(self._TASKS_FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['task_id', 'task', 'created_at', 'priority'])
        
        if not os.path.exists(self._COMPLETE_TASKS_FILE):
            with open(self._COMPLETE_TASKS_FILE, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['task_id', 'task', 'created_at', 'completed_at'])

    def _load_tasks_file(self, filename):
        tasks_list = []
        if not os.path.exists(filename):
            return []
        
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks_list.append(row)
        return tasks_list
    
    def _save_tasks_file(self, filename, tasks_list):
        with open(filename, 'w', newline='') as file:
            if filename == self._TASKS_FILE:
                fieldnames = ['task_id', 'task', 'created_at', 'priority']
            else:
                fieldnames = ['task_id', 'task', 'created_at', 'completed_at']
            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tasks_list)
    
    def _add_task_to_tasks_file(self):
        print(self.white + '\n ======== Add a new task ======== \n')
        
        add_task_input = input(self.white + "Add new task: ").strip()
        
        if not add_task_input:
            return self.red + '\nYour input was empty!'

        tasks = self._load_tasks_file(self._TASKS_FILE)
        
        new_task = {
            'task_id': len(tasks) + 1,
            'task': add_task_input,
            'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'priority': 'medium'  # Default priority
        }

        tasks.append(new_task)
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
                print(self.cyan + f'*{index}: {task["task"]} (Priority: {task["priority"]})')

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
            deleted_task = tasks.pop(delete_task_input-1)  # Adjust for 0-based index
            
            # Reassign task IDs to maintain sequence
            for idx, task in enumerate(tasks, start=1):
                task['task_id'] = idx
                
            self._save_tasks_file(self._TASKS_FILE, tasks)  # Persist changes

            return self.green + f"\nTask '{deleted_task['task']}' has been deleted"
        
        else:  # No tasks case
            return self.red + "\nThe tasks list is empty!"

    def _display_tasks_list(self):
        # Load current tasks from file using helper function
        tasks = self._load_tasks_file(self._TASKS_FILE)

        # Check if tasks exist
        if tasks:
            # Display section header with consistent formatting
            print(self.white + '\n======== Your Tasks ======== \n')
            
            # Calculate column widths for nice formatting
            id_width = len(str(len(tasks))) + 2
            task_width = max(len(task['task']) for task in tasks) + 2
            priority_width = 10
            
            # Print column headers
            header = (f"{self.cyan}{'#'.ljust(id_width)}"
                    f"{'Task'.ljust(task_width)}"
                    f"{'Priority'.ljust(priority_width)}"
                    f"{'Created At'}")
            print(header)
            print('-' * (id_width + task_width + priority_width + 15))
            
            # Enumerate and display each task with enhanced formatting
            for index, task in enumerate(tasks, start=1):
                # Format: "1. Task description [Priority] (creation date)"
                task_line = (f"{self.white}{str(index).ljust(id_width)}"
                            f"{task['task'].ljust(task_width)}"
                            f"{self.magenta}{task['priority'].ljust(priority_width)}"
                            f"{self.cyan}{task['created_at']}")
                print(task_line)
            
            # Return success confirmation message
            return self.green + f"\nDisplaying {len(tasks)} tasks."

        else:
            # Return empty list warning message
            return self.red + "\nYour task list is empty!"

    def _mark_task_as_complete_task(self):
        # Load current tasks and completed tasks
        tasks = self._load_tasks_file(self._TASKS_FILE)
        complete_tasks = self._load_tasks_file(self._COMPLETE_TASKS_FILE)
        
        # Only proceed if there are tasks to complete
        if tasks:
            # Display completion section header
            print(self.white + '\n======== Mark Task as Completed ======== \n')
            
            # Show all tasks with selection numbers
            for index, task in enumerate(tasks, start=1):
                print(self.cyan + f'{index}. {task["task"]} [Priority: {task["priority"]}]')

            # Get user input for task to complete
            complete_task_input = input(self.white + '\nSelect the number to mark as completed (or "q" to quit): ').strip()

            # Allow user to quit
            if complete_task_input.lower() == 'q':
                return self.magenta + "\nOperation cancelled."

            try:
                # Convert and validate input
                task_index = int(complete_task_input)
                             
                # Custom validation checks
                if task_index == 0:
                    raise ZeroUserInput(message='Task numbering starts at 1.')
                
                if task_index < 0:
                    raise NegetiveInputNumber(message='Please enter a positive number.')
                
                if task_index > len(tasks):
                    raise TasksInputOutOfRangeError(
                        message=f"\nError: Maximum task number is {len(tasks)}.",
                        len_tasks_list=len(tasks)
                    )
                    
                # Get the task to be completed
                completed_task = tasks[task_index-1]
                
                # Add completion timestamp
                completed_task['completed_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Remove priority field as it's no longer needed
                if 'priority' in completed_task:
                    del completed_task['priority']
                
                # Move task from active to completed
                complete_tasks.append(completed_task)
                tasks.pop(task_index-1)
                
                # Update task IDs for remaining tasks
                for idx, task in enumerate(tasks, start=1):
                    task['task_id'] = idx
                
                # Persist changes to both files
                self._save_tasks_file(self._TASKS_FILE, tasks)
                self._save_tasks_file(self._COMPLETE_TASKS_FILE, complete_tasks)

                return self.green + f"\nTask '{completed_task['task']}' marked as completed."

            # Handle various error cases
            except ValueError:  # Non-integer input
                return self.red + "\nError: Please enter a valid number or 'q' to quit."

            except TasksInputOutOfRangeError as e:
                return self.red + f'{e.message}'

            except NegetiveInputNumber as e:
                return self.red + f'\n{e.message}'

            except ZeroUserInput as e:
                return self.red + f'\n{e.message}'

        else:  # No tasks case
            return self.red + "\nYour active tasks list is empty!"
    
    def _edit_task_in_tasks_list(self):
        # Load current tasks from file
        tasks = self._load_tasks_file(self._TASKS_FILE)
        
        # Only proceed if tasks exist
        if tasks:
            # Display edit section header
            print(self.white + '\n======== Edit Task ======== \n')
            
            # Display all tasks with numbering and details
            for index, task in enumerate(tasks, start=1):
                print(self.cyan + f'{index}. {task["task"]} [Priority: {task["priority"]}]')
            
            # Get user input for task to edit
            edit_task_input = input(self.white + '\nSelect the number to edit (or "q" to quit): ').strip()

            # Allow user to cancel operation
            if edit_task_input.lower() == 'q':
                return self.magenta + "\nEdit operation cancelled."

            try:
                # Convert and validate input
                task_index = int(edit_task_input)
                
                # Custom validation checks
                if task_index == 0:
                    raise ZeroUserInput(message='Task numbering starts at 1.')
                
                if task_index < 0:
                    raise NegetiveInputNumber(message='Please enter a positive number.')
                
                if task_index > len(tasks):
                    raise TasksInputOutOfRangeError(
                        message=f"\nError: Maximum task number is {len(tasks)}.",
                        len_tasks_list=len(tasks)
                    )
                
                # Get the task to be edited
                task_to_edit = tasks[task_index-1]
                
                # Display current task details
                print(self.white + f'\nCurrent Task: {task_to_edit["task"]}')
                print(self.white + f'Current Priority: {task_to_edit["priority"]}')
                
                # Get new task details
                new_task_text = input(self.white + 'Enter new task text (press Enter to keep current): ').strip()
                new_priority = input(self.white + 'Enter new priority (high/medium/low, Enter to keep current): ').strip().lower()
                
                # Update task if new values provided
                if new_task_text:
                    task_to_edit['task'] = new_task_text
                if new_priority in ('high', 'medium', 'low'):
                    task_to_edit['priority'] = new_priority
                elif new_priority:  # Invalid priority entered
                    return self.red + "\nInvalid priority - keeping current value."
                
                # Save the updated task list
                self._save_tasks_file(self._TASKS_FILE, tasks)
                
                return self.green + f"\nTask {task_index} updated successfully."

            # Handle various error cases
            except ValueError:  # Non-integer input
                return self.red + "\nError: Please enter a valid number or 'q' to quit."
            
            except TasksInputOutOfRangeError as e:
                return self.red + f'{e.message}'
            
            except NegetiveInputNumber as e:
                return self.red + f'\n{e.message}'
            
            except ZeroUserInput as e:
                return self.red + f'\n{e.message}'

        else:  # No tasks case
            return self.red + "\nYour tasks list is empty!"
         
    def _search_task_in_tasks_list(self):
        # Load both active and completed tasks
        tasks = self._load_tasks_file(self._TASKS_FILE)
        complete_tasks = self._load_tasks_file(self._COMPLETE_TASKS_FILE)

        # Display search header
        print(self.white + '\n======== Search Tasks ======== \n')
        print(self.cyan + "Search options:")
        print(self.cyan + "1. Search by keyword")
        print(self.cyan + "2. Search by priority")
        print(self.cyan + "3. Search by date range\n")

        search_option = input(self.white + 'Choose search option (1-3): ').strip()

        # Initialize search results flag
        found = False

        # Check if both lists are empty
        if not tasks and not complete_tasks:
            return self.red + "\nNo tasks exist yet."

        try:
            if search_option == '1':
                # Keyword search
                search_term = input(self.white + 'Enter search keyword: ').strip().lower()
                if not search_term:
                    return self.red + "\nSearch term cannot be empty."

                print(self.white + '\n=== Search Results ===\n')

                # Search active tasks
                for task in tasks:
                    if search_term in task['task'].lower():
                        found = True
                        print(self.green + f"[Active] {task['task']} (Priority: {task['priority']}, Created: {task['created_at']})")

                # Search completed tasks
                for task in complete_tasks:
                    if search_term in task['task'].lower():
                        found = True
                        print(self.magenta + f"[Completed] {task['task']} (Created: {task['created_at']}, Completed: {task['completed_at']})")

            elif search_option == '2':
                # Priority search
                priority = input(self.white + 'Enter priority (high/medium/low): ').strip().lower()
                if priority not in ['high', 'medium', 'low']:
                    return self.red + "\nInvalid priority level."

                print(self.white + f'\n=== Tasks with {priority} priority ===\n')

                # Search active tasks by priority
                for task in tasks:
                    if task['priority'].lower() == priority:
                        found = True
                        print(self.green + f"[Active] {task['task']} (Created: {task['created_at']})")

            elif search_option == '3':
                # Date range search
                start_date = input(self.white + 'Enter start date (YYYY-MM-DD) or leave blank: ').strip()
                end_date = input(self.white + 'Enter end date (YYYY-MM-DD) or leave blank: ').strip()

                print(self.white + '\n=== Tasks in date range ===\n')

                # Search active tasks by date
                for task in tasks:
                    task_date = task['created_at'].split()[0]  # Get date part only
                    if (not start_date or task_date >= start_date) and (not end_date or task_date <= end_date):
                        found = True
                        print(self.green + f"[Active] {task['task']} (Created: {task['created_at']})")

                # Search completed tasks by date
                for task in complete_tasks:
                    task_date = task['completed_at'].split()[0]  # Get date part only
                    if (not start_date or task_date >= start_date) and (not end_date or task_date <= end_date):
                        found = True
                        print(self.magenta + f"[Completed] {task['task']} (Completed: {task['completed_at']})")

            else:
                return self.red + "\nInvalid search option."

            if not found:
                return self.red + "\nNo matching tasks found."

            return self.green + "\nSearch completed successfully."

        except Exception as e:
            return self.red + f"\nError during search: {str(e)}"
    
    def _clear_all_tasks_in_tasks_list(self):
        # Load current tasks from file
        tasks = self._load_tasks_file(self._TASKS_FILE)
        complete_tasks = self._load_tasks_file(self._COMPLETE_TASKS_FILE)

        # Display clear tasks header with warning
        print(self.white + "\n======== Clear All Tasks ========\n")
        print(self.red + "WARNING: This will permanently delete ALL active tasks!")
        print(self.white + f"Total tasks to be deleted: {len(tasks)}\n")

        # Only proceed if tasks exist
        if tasks:
            # Get confirmation from user with multiple checks
            confirm1 = input(self.white + "Type 'DELETE' to confirm: ").strip().upper()
            if confirm1 != "DELETE":
                return self.magenta + "\nFirst confirmation failed - operation cancelled."

            confirm2 = input(self.white + "Are you absolutely sure? (y/n): ").strip().lower()
            if confirm2 not in ['y', 'yes']:
                return self.magenta + "\nSecond confirmation failed - operation cancelled."

            # Create backup before clearing
            backup_file = f"tasks_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            self._save_tasks_file(backup_file, tasks)
            
            # Clear the task list in memory
            tasks.clear()
            
            # Save the empty list to file
            self._save_tasks_file(self._TASKS_FILE, tasks)
            
            return (self.green + "\nAll tasks cleared successfully." +
                    self.cyan + f"\nBackup saved as: {backup_file}")

        else:  # No tasks case
            return self.red + "\nYour active tasks list is already empty!"
        

    def _display_complete_task_list(self):
        # Load completed tasks from persistent storage
        complete_tasks = self._load_tasks_file(self._COMPLETE_TASKS_FILE)
        
        # Display section header for completed tasks
        print(self.white + '\n======== Completed Tasks ======== \n')

        # Check if there are completed tasks to display
        if complete_tasks:
            # Calculate column widths for nice formatting
            id_width = len(str(len(complete_tasks))) + 2
            task_width = max(len(task['task']) for task in complete_tasks) + 2
            date_width = 20
            
            # Print column headers
            print(self.cyan + 
                f"{'#'.ljust(id_width)}"
                f"{'Task'.ljust(task_width)}"
                f"{'Completed On'.ljust(date_width)}"
                f"{'Originally Created'}")
            print('-' * (id_width + task_width + date_width + 18))
            
            # Enumerate and display each task with enhanced formatting
            for num, task in enumerate(complete_tasks, start=1):
                print(self.white + f"{str(num).ljust(id_width)}"
                    f"{task['task'].ljust(task_width)}"
                    f"{self.magenta}{task['completed_at'].ljust(date_width)}"
                    f"{self.cyan}{task['created_at']}")
            
            # Display statistics
            print(self.green + f"\nTotal completed tasks: {len(complete_tasks)}")
            
            # Calculate completion time statistics if available
            try:
                completion_times = []
                for task in complete_tasks:
                    created = datetime.datetime.strptime(task['created_at'], '%Y-%m-%d %H:%M:%S')
                    completed = datetime.datetime.strptime(task['completed_at'], '%Y-%m-%d %H:%M:%S')
                    completion_times.append((completed - created).days)
                
                if completion_times:
                    avg_days = sum(completion_times) / len(completion_times)
                    print(self.green + f"Average completion time: {avg_days:.1f} days")
            except:
                pass  # Skip statistics if date parsing fails

            return ""

        else:
            # Return message when no completed tasks exist
            return self.red + "\nNo tasks have been completed yet."
        
    def start(self):
        # Initialize files with CSV headers if they don't exist
        for file, fields in [
            (self._TASKS_FILE, ['task_id', 'task', 'created_at', 'priority']),
            (self._COMPLETE_TASKS_FILE, ['task_id', 'task', 'created_at', 'completed_at'])
        ]:
            if not os.path.exists(file):
                with open(file, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()

        while True:
            # Clear screen for better UX (works on both Windows and Unix)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display menu options with consistent formatting
            print(self.white + "\n" + "═"*40)
            print(self.white + " Main Menu ".center(40, "─"))
            print(self.white + "═"*40)
            print(self.green + "1. Add a new task")
            print(self.red + "2. Delete a task")
            print(self.cyan + "3. List active tasks")
            print(self.magenta + "4. Mark task as completed")
            print(self.white + "5. Edit a task")
            print(self.cyan + "6. Search tasks")
            print(self.red + "7. Clear all active tasks")
            print(self.magenta + "8. List completed tasks")
            print(self.white + "9. View statistics")
            print(self.red + "0. Quit")
            print(self.white + "═"*40)

            # Get user input with timeout for auto-exit
            try:
                user_option_input = input(self.white + "\nEnter your choice (0-9): ").strip().lower()
                
                # Allow alternate quit commands
                if user_option_input in ['q', 'quit', 'exit', '0']:
                    print(self.magenta + "\nGoodbye! 👋")
                    break
                    
                # Convert to integer and validate
                user_option_input = int(user_option_input)
                if user_option_input not in range(0, 10):
                    raise UserOptionInputError(
                        message="\nInvalid input. Please enter a number between 0-9. Your input was ",
                        num_input=user_option_input,
                    )
                
                # Process user choice
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen before action
                
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
                        self._display_statistics()
                    
                input(self.white + "\nPress Enter to continue...")  # Pause before returning to menu
                
            except ValueError:
                print(self.red + '\nInvalid input. Please enter a number.')
                datetime.sleep(1)  # Brief pause before showing menu again
                
            except UserOptionInputError as e:
                print(self.red + f"{e.message}{e.num_input}")
                datetime.sleep(1)

if __name__ == "__main__":
    app = ToDoList()
    app.start()