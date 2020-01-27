from NsfwClassifier import main
import os
import easygui
directories = []
arguments = []
delete_sfw = False
delete_nsfw = False
delete_other = False
same_dir = False


def menu():
    clear()
    global delete_nsfw
    global delete_sfw
    global delete_other
    global same_dir
    global arguments

    print("=====[NSFWClassifier]=====")
    print("Select an option:")

    choice = input(str.format("""
    1: Select Directories
    Arguments:
    2: [{}] Delete NSFW - Deletes NSFW files.
    3: [{}] Delete SFW - Deletes SFW files.
    4: [{}] Delete other - Deletes non image files:
    5: [{}] Do not move files into 'NSFW' or 'SFW' folders.
    
    6: Start
    7: Exit
    
    Input Number [1-6]:
    """, 'X' if delete_nsfw is True else ' ', 'X' if delete_sfw is True else ' ', 'X' if delete_other is True else ' ',
                              'X' if same_dir is True else ' '))

    if choice == str(1):
        directory_menu()
    elif choice == str(2):
        if delete_sfw is True:
            try:
                arguments.remove('--delete-sfw')
            except ValueError:
                pass
            delete_sfw = False

        if delete_nsfw is False:
            arguments.append('--delete-nsfw')
            delete_nsfw = True
        else:
            try:
                arguments.remove('--delete-nsfw')
            except ValueError:
                pass
            delete_nsfw = False
    elif choice == str(3):
        if delete_nsfw is True:
            try:
                arguments.remove('--delete-nsfw')
            except ValueError:
                pass
            delete_nsfw = False

        if delete_sfw is False:
            arguments.append('--delete-sfw')
            delete_sfw = True
        else:
            try:
                arguments.remove('--delete-sfw')
            except ValueError:
                pass
            delete_sfw = False
    elif choice == str(4):
        if delete_other is False:
            arguments.append('--delete-other')
            delete_other = True
        else:
            try:
                arguments.remove('--delete-other')
            except ValueError:
                pass
            delete_other = False
    elif choice == str(5):
        if same_dir is False:
            arguments.append('--same-dir')
            same_dir = True
        else:
            try:
                arguments.remove('--same-dir')
            except ValueError:
                pass
            same_dir = False
    elif choice == str(6):
        if len(directories) == 0:
            print("No directories specified!")
            input("Press Enter to continue...")
            menu()

        argument_list = ["--dirs"]
        for arg in directories:
            argument_list.append(arg)
        for arg in arguments:
            argument_list.append(arg)
        main(argument_list)
    elif choice == str(7):
        exit(0)

    clear()
    menu()

def directory_menu():
    clear()
    print("Directory Selector")

    if len(directories) is not 0:
        count = 0
        for dir in directories:
            count += 1
            print(str.format("{}: {}", count, dir))
    else:
        print("No directories specified.")
    print("")

    choice = input("""
    1. Add new directory.
    2. Delete directory
    3. Clear all
    4. Go back.
    """)

    if choice == str(1):
        path = easygui.diropenbox()
        if os.path.isdir(path):
            for dir in directories:
                if path == dir:
                    print("Directory already exists!")
                    input("Press Enter to continue...")
                    directory_menu()
            directories.append(path)
        else:
            print("Not a directory")
    elif choice == str(2):
        choice = input("Select number: ")
        try:
            int(choice)
        except ValueError:
            print("Input is not a number.")
            input("Press Enter to continue...")
            directory_menu()
        try:
            del directories[int(choice) - 1]
        except IndexError:
            print("Specified number does not exist!")
            input("Press Enter to continue...")
            directory_menu()
    elif choice == str(3):
        directories.clear()
        directory_menu()
    elif choice == str(4):
        menu()
    clear()
    directory_menu()


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
menu()
