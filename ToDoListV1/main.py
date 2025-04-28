if __name__ == "__main__":
    
    # Initialize lists to store tasks
    tasks = []
    complete_tasks = []

    print("Welcome to the To-Do List App :)")

    while True:
        # Display the main menu
        print("\n")
        print("Please select one of the following options")
        print("------------------------------------------")
        print("1. Add a new task")
        print("2. Delete a task")
        print("3. List tasks")
        print("4. Mark task as completed")
        print("5. Edit a task")
        print("6. Search tasks")
        print("7. Clear all tasks")
        print("8. List completed tasks")
        print("9. Quit")

        # Get user input for menu choice
        user_input = input(": ")

        # Option 1: Add a new task
        if user_input == '1':
            print('\n ======== Add a new task ======== \n'.title())
            add_task_input = input("Add new task: ")
            tasks.append(add_task_input)
            print("Your task has been added succssfully.")
        
        # Option 2: Delete a task
        elif user_input == '2':
            if tasks:
                print('\n======== Delete a task ======== \n'.title())
                for word, task in enumerate(tasks):
                    print(f'*{word}: {task}')
                delete_task_input =  int(input('Select the * number to delete the task: '))
                del tasks[delete_task_input]
                print("\nThe task number {} has been deleted".format(delete_task_input))
            else:
                print("The tasks list is empty.")
        
        # Option 3: List all current tasks
        elif user_input == '3':
            print('\n======== List tasks ======== \n'.title())
            if tasks:
                num = 1
                for task in tasks:
                    print(f'{num}.{task}\n')
                    num += 1
            else:
                print("The tasks list is empty.")
        
        # Option 4: Mark a task as completed
        elif user_input == '4':
            print('\n======== Mark task as completed ======== \n'.title())
            for word, task in enumerate(tasks):
                print(f'+{word}: {task}')

            complete_task_input = int(input('Select the + number to add the task to complete tasks list: '))
            complete_tasks.append(tasks[complete_task_input])
            del tasks[complete_task_input]
            print("\nThe complete tasks has been modified.")

            print("\nComplete task list:\n")
            print(complete_tasks)

        # Option 5: Edit a task
        elif user_input == '5':
            print('\n======== Edit a task ======== \n'.title())
            for word, task in enumerate(tasks):
                print(f'#{word}: {task}')

            edit_task_input = int(input('Select the # number to edit: '))
            new_task_input = input('\n Edit the task: ')
            tasks[edit_task_input] = new_task_input
            print("\nThe tasks has been modified.")

        # Option 6: Search for a task
        elif user_input == '6':
            print('\n======== Search tasks ======== \n'.title())
            search_user_input = input('Search: ')
            if not tasks:
                print("\nThe tasks list is empty\n")

            if search_user_input in tasks:
                index = tasks.index(search_user_input)
                print(f'Task number {index}: ', end='')
                print(tasks[index])
            
            elif search_user_input in complete_tasks:
                index = complete_tasks.index(search_user_input)
                print(f'Completed task number {index}: ', end='')
                print(complete_tasks[index])

            else:
                print("Can not find the task.")

        # Option 7: Clear all current tasks
        elif user_input == '7':
            print("\n======== Clear all tasks ========\n".title())
            if tasks:
                user_input = input("Are you sure (y/n)? ")
                if user_input.lower() in ['y', 'yes']:
                    tasks.clear()
                    print("\n The tasks list has benn emptied.")
            else:
                print("The tasks list is empty.")

        # Option 8: List completed tasks
        elif user_input == '8':
            print('\n======== List completed tasks ======== \n'.title())
            if complete_tasks:  # <- Fixed bug: changed from `if tasks` to `if complete_tasks`
                num = 1
                for task in complete_tasks:
                    print(f'{num}.{task}\n')
                    num += 1
            else:
                print("The completed tasks list is empty.")

        # Option 9 or Q/q: Quit the program
        elif user_input in ['q', 'Q', '9']:
            break
