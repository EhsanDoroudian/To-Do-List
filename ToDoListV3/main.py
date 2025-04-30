import os
import datetime
import colorama
from colorama import Fore, Back, Style

from exceptions import UserOptionInputError, TasksInputOutOfRangeError, NegetiveInputNumber, ZeroUserInput

colorama.init()
print(Fore.RED + "This text is red!")
print(Fore.GREEN + "This text is green!")


print(Fore.RED + 'This text is red')
print(Back.GREEN + 'This text has a green background')
print(Style.BRIGHT + 'This text is bright')
print(Style.RESET_ALL + 'Back to normal text')


# Print text with different colors and styles
print(Style.BRIGHT + Fore.RED + Back.GREEN + 'Bright red text on green background')


print(Style.BRIGHT + "This text is bright/bold")
print(Style.DIM + "This text is dim")
print(Style.NORMAL + "This text is normal")


print(Fore.RED + 'Red text')
# This will still be red
print('Normal text')  
# Reset styles
print(Style.RESET_ALL)  
print('Back to normal')


class ToDoList:

    bold = Style.BRIGHT
    white = Fore.WHITE + bold
    red = Fore.RED + bold
    green = Fore.GREEN + bold
    magenta = Fore.MAGENTA + bold

    def __init__(self, tasks_file="tasks.txt", completed_tasks_file="complete_tasks.txt"):
        self._TASKS_FILE = tasks_file
        self._COMPLETE_TASKS_FILE = completed_tasks_file
        self._tasks = []
        self._complete_list = []
        self._create_date = datetime.datetime.now()
        self._number_of_tasks = 0

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
                # case 2:
                #     print(delete_task_from_tasks_list())
                # case 3:
                #     print(display_tasks_list())
                # case 4:
                #     print(mark_task_as_complete_task())
                # case 5:
                #     print(edit_task_in_tasks_list())
                # case 6:
                #     print(search_task_in_tasks_list())
                # case 7:
                #     print(clear_all_tasks_in_tasks_list())
                # case 8:
                #     print(display_complete_task_list())
                # case 9:
                #     cprint("\nGoodBye👋", color='magenta',attrs=['bold'])
                #     break

if __name__ == "__main__":
    app = ToDoList()
    app.start()