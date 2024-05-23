import os
import getpass
import base64
import argon2
from cryptography.fernet import Fernet
import pyperclip

HOME = os.path.expanduser("~")
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
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
    choice = input()
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
        delete()
    elif choice_int == 4:
        return False
    elif choice_int == 0:
        advanced()
    else:
        print("Invalid choice")
    return True


def advanced():
    print("Advanced Options")
    print("1. Initialize")
    print("2. Export all passwords")
    choice = input()

    try:
        choice_int = int(choice)
    except ValueError:
        print("Invalid Input (not a number)")
        return

    if choice_int == 1:
        init()
    elif choice_int == 2:
        export()
    else:
        print("Invalid choice")
    return


def export():
    os.system("cp -r " + INIT_PATH + " " + os.path.join("pass_export"))
    os.system(f"tar cfz pass_export.tar.gz pass_export ")
    os.system(f"rm -r pass_export")
    os.system("clear")
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
    while again:
        again = run(cipher)


def isInitialized():
    return os.path.exists(INIT_PATH)


def view(cipher):
    path_followed = INIT_PATH
    if not os.listdir(path_followed):
        print("Nothing Stored")
        return
    go_deeper = True
    while go_deeper:
        l = [
            x
            for x in os.listdir(path_followed)
            if os.path.isdir(os.path.join(path_followed, x))
        ]
        l.sort()
        if not l:
            break
        for i, item in enumerate(l):
            print(str(i + 1) + ". " + item)
        choice = input("\n ")
        os.system("clear")
        try:
            choice_int = int(choice)
        except ValueError:
            print("Invalid Input (not a number)")
            continue
        if choice_int > len(l):
            print("Invalid Choice")
            continue
        if choice_int == 0:
            return
        path_followed = os.path.join(path_followed, l[choice_int - 1])

    for item in os.listdir(path_followed):
        all_files = os.listdir(path_followed)
        for i, file in enumerate(all_files):
            print(str(i + 1) + ". " + file)
        choice = input("\n ")
        os.system("clear")
        try:
            choice_int = int(choice)
        except ValueError:
            print("Invalid Input (not a number)")
            continue
        if choice_int > len(all_files):
            print("Invalid Choice")
            continue
        with open(os.path.join(path_followed, all_files[choice_int - 1]), "rb") as f:
            try:
                pyperclip.copy(cipher.decrypt(f.read()).decode())
                print(bcolors.OKGREEN + "Copied to clipboard" + bcolors.ENDC)
                exit(0)
            except Exception as e:
                print(bcolors.FAIL + "incorrect key ig" + bcolors.ENDC)
                exit(1)
    return


def init():
    if isInitialized():
        os.system("clear")
        print("Already initialized")
        return
    else:
        os.makedirs(INIT_PATH)
        os.system("clear")
        print("Initialized at " + INIT_PATH)


def add(cipher):
#     find .pass_store -type d -print0 | while IFS= read -r -d '' dir; do
#   if [ -z "$(find "$dir" -mindepth 1 -type d 2>/dev/null)" ]; then
#     echo "$dir"
#   fi
# done
    print("Existing DIRs:")
    PWD = os.getcwd()
    os.system("cd " + INIT_PATH)

    cmd = "find . -type d -print0 | while IFS= read -r -d '' dir; do if [ -z \"$(find \"$dir\" -mindepth 1 -type d 2>/dev/null)\" ]; then echo \"$dir\"; fi; done"
    os.system(cmd)
    os.system("cd " + PWD)
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


if __name__ == "__main__":
    main()
