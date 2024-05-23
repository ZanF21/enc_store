import os
import getpass
import base64
import argon2
from cryptography.fernet import Fernet
import pyperclip

HOME = os.path.expanduser("~")
CURR_DIR = os.getcwd()
INIT_PATH = os.path.join(HOME, ".pass_store")


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def run(cipher):
    if not isInitialized():
        init()
    print("1. View\n2. Add\n3. Delete\n4. Exit")
    choice = input(": ")
    os.system("clear")

    try:
        choice_int = int(choice)
    except ValueError:
        print("Invalid Input (not a number)")
        return True

    if choice_int == 1:
        view(cipher)
    elif choice_int == 2:
        add(cipher)
    elif choice_int == 3:
        delete(cipher)
    elif choice_int == 4:
        return False
    elif choice_int == 0:
        advanced()
    else:
        print("Invalid choice")
    return True


def advanced():
    print("Advanced Options")
    print("1. Initialize\n2. Export\n3. List All\n0. Go back")
    choice = input(": ")
    os.system("clear")
    try:
        choice_int = int(choice)
    except ValueError:
        print(bcolors.FAIL + "Invalid Input (not a number)" + bcolors.ENDC)
        return

    if choice_int == 1:
        init()
    elif choice_int == 2:
        export()
    elif choice_int == 3:
        list_all()
    elif choice_int == 0:
        return
    else:
        print(bcolors.FAIL + "Invalid choice, going back" + bcolors.ENDC)
    return


def list_all():
    os.chdir(INIT_PATH)
    print("All Stored Passwords:")
    os.system("tree . --noreport")
    os.chdir(CURR_DIR)
    print("\n")
    return


def export():
    os.system("cp -r " + INIT_PATH + " " + os.path.join(CURR_DIR, "pass_export"))
    os.system(f"tar cfz pass_export.tar.gz pass_export")
    os.system(f"rm -r pass_export")
    print(f"Exported to {os.path.join(CURR_DIR, 'pass_export.tar.gz')}")


def cipher_gen(prompt="Password: "):
    key = argon2.low_level.hash_secret_raw(
        getpass.getpass(prompt).encode(),
        salt=b"ZigZagZanZark",
        time_cost=1,
        memory_cost=8,
        parallelism=1,
        hash_len=32,
        type=argon2.low_level.Type.D,
    )
    assert 32 == len(key)
    b64_key = base64.urlsafe_b64encode(key)
    cipher = Fernet(b64_key)
    return cipher


def main():
    again = True
    cipher = cipher_gen()
    os.system("clear")
    while again:
        again = run(cipher)


def isInitialized():
    return os.path.exists(INIT_PATH)


def view(cipher):
    try:
        path = select_file()
        with open(path, "rb") as f:
            try:
                pyperclip.copy(cipher.decrypt(f.read()).decode())
                short_path = path[len(INIT_PATH) + 1 :]
                print(
                    bcolors.OKGREEN + f"Copied {short_path} to clipboard" + bcolors.ENDC
                )
                exit(0)
            except Exception as e:
                print(bcolors.FAIL + "incorrect key ig" + bcolors.ENDC)
                exit(0)

    except Exception as e:
        print(e)
        return


def init():
    if isInitialized():
        print("Already initialized")
        return
    else:
        os.makedirs(INIT_PATH)
        print(bcolors.OKGREEN + "Initialized at " + INIT_PATH + bcolors.ENDC + "\n")


def add(cipher):
    print("Existing DIRs:")
    os.chdir(INIT_PATH)
    os.system(f"tree . -d --noreport")
    os.chdir(CURR_DIR)
    print("\n")
    enc_path = input("Which DIR: ")
    file_name = input("Username: ")

    exact_path = os.path.join(INIT_PATH, enc_path)
    os.makedirs(os.path.dirname(exact_path + "/"), exist_ok=True)

    imp_stuff = input("Enter stuff: ")
    enc_stuff = cipher.encrypt(imp_stuff.encode())
    with open(os.path.join(exact_path, file_name), "wb+") as f:
        f.write(enc_stuff)
    os.system("clear")
    print("Added")


def select_file():
    path_followed = INIT_PATH

    if not os.listdir(path_followed):
        raise Exception(bcolors.OKBLUE + "Nothing Stored" + bcolors.ENDC)

    go_deeper = True
    while go_deeper:
        l = [
            x
            for x in os.listdir(path_followed)
            if os.path.isdir(os.path.join(path_followed, x))
        ]
        l.sort()
        if not l:
            go_deeper = False
            continue  # basically a break, wrote it this way for readability

        for i, item in enumerate(l):
            print(str(i + 1) + ". " + item)
        choice = input("\n: ")
        os.system("clear")
        try:
            choice_int = int(choice)
        except ValueError:
            print(bcolors.FAIL + "Invalid Input (not a number)" + bcolors.ENDC)
            continue

        if choice_int > len(l):
            print(bcolors.FAIL + "Invalid Choice" + bcolors.ENDC)
            continue
        if choice_int == 0:
            raise Exception(bcolors.OKCYAN + "User Exited" + bcolors.ENDC)

        path_followed = os.path.join(path_followed, l[choice_int - 1])

    while True:
        all_files = os.listdir(path_followed)
        for i, file in enumerate(all_files):
            print(str(i + 1) + ". " + file)
        choice = input("\n ")
        os.system("clear")
        try:
            choice_int_file = int(choice)
        except ValueError:
            print(bcolors.FAIL + "Invalid Input (not a number)" + bcolors.ENDC)
            continue

        if choice_int_file > len(all_files):
            print(bcolors.FAIL + "Invalid Choice" + bcolors.ENDC)
            continue
        if choice_int_file == 0:
            raise Exception(bcolors.OKCYAN + "User Exited" + bcolors.ENDC)
        break

    return os.path.join(path_followed, all_files[choice_int_file - 1])


def delete(cipher):
    try:
        path = select_file()
        with open(path, "rb") as f:
            try:
                pyperclip.copy(cipher.decrypt(f.read()).decode())
                os.remove(path)
                short_path = path[len(INIT_PATH) + 1 :]
                os.system("find " + INIT_PATH + " -type d -empty -delete")
                print(
                    bcolors.OKGREEN
                    + f"Deleted {short_path} and copied to clipboard (just in case)"
                    + bcolors.ENDC
                )
            except Exception as e:
                print(bcolors.FAIL + "incorrect key ig" + bcolors.ENDC)
                exit(0)
    except Exception as e:
        print(e)
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCTRL+C, exiting")
        exit(0)
    except EOFError:
        print("\nCTRL+D, exiting")
        exit(0)
