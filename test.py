import os

# get list of dirs in current path

print("Get File")

final_path = ""

CURR_PATH = os.getcwd()
HOME_DIR = os.getenv("HOME")

while True:
    path = input()
    if path == ".":
        final_path = CURR_PATH
        break
    elif path == "/":
        final_path = HOME_DIR
        break
    else:
        print("Invalid Path (only '.' [CURR_DIR] and '/' [HOME_DIR] allowed)")

file_selected = False

while not file_selected:
    ls_dir_only = [
        x
        for x in os.listdir(final_path)
        if os.path.isdir(os.path.join(final_path, x)) and not x.startswith(".")
    ]
    ls_files_only = [
        x
        for x in os.listdir(final_path)
        if not os.path.isdir(os.path.join(final_path, x)) and not x.startswith(".")
    ]
    ls_dir_only.sort()
    ls_files_only.sort()

    print("\nPath: " + final_path + "\n")
    print("00. Go back to previous directory")
    i = 1

    for item in ls_dir_only:
        print(f"{i:02}. {item}/")
        i += 1
    for item in ls_files_only:
        print(f"{i:02}. {item}")
        i += 1
    if len(ls_dir_only) == 0 and len(ls_files_only) == 0:
        print("No files or directories in this path")
        exit(1)

    while True:
        choice = input("\n: ")
        try:
            choice_int = int(choice)
            if choice_int == 0:
                print("Going back to previous directory")
                final_path = os.path.dirname(final_path)
                break
            if choice_int >= i or choice_int < 1:
                print("Invalid Choice (Pick inside the range)")
                continue
            break
        except ValueError:
            print("Invalid Input (not a number)")
            continue

    if choice_int == 0:
        continue
    elif choice_int <= len(ls_dir_only):
        final_path = os.path.join(final_path, ls_dir_only[choice_int - 1])
    else:
        file_selected = True
        final_path = os.path.join(
            final_path, ls_files_only[choice_int - 1 - len(ls_dir_only)]
        )

print(final_path)

exit(0)
