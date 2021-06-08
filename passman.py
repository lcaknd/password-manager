import os
import getpass
import json
import pathlib
import datetime
import subprocess
import sys
import string
import random
import array
import time
import pyperclip

HOME = str(pathlib.Path.home())  # path for saving all password related information


def master_password_update(password, last_access):
    """
    Function employed in updating the last_access time of the master_password
    :param password: master password (str)
    :param last_access: last_access time of the application
    :return: None
    """
    temp = {
        "password": password,
        "last_access": last_access
    }
    with open(HOME + "\\master_password.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(temp))


def read_master_password_file():
    """
    Function employed in checking if last time to enter master password is greater than 24 hours
    or not
    :return: True or False (bool)
    """
    master_password = {}
    found = False
    try:
        with open(HOME + "/master_password.json", "r", encoding="utf-8") as file:  # opening master password file
            file_data = json.loads(file.read())
            master_password["password"] = file_data.get("password")
            master_password["last_access"] = file_data.get("last_access")
            found = True

    except FileNotFoundError:
        found = False
    finally:
        if found:  # if file exists then ask for master password only if last_access is greater than 24 hours
            print()
            if (datetime.datetime.now() - datetime.datetime.strptime(master_password["last_access"],
                                           "%Y-%m-%d %H:%M:%S")).total_seconds() // 3600 > 24:

                password = getpass.getpass(prompt="Enter your master password: ")
                if password == master_password["password"]:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    master_password_update(password, current_time)
                    return True
                else:
                    return False
            else:
                return True

        else:  # if file is not found then create the file
            password = getpass.getpass(prompt="Create your master password: ")
            re_enter_password = getpass.getpass(prompt="Re-enter your master password: ")

            while password != re_enter_password:  # ask for password until password1 is not matching with password2
                password = getpass.getpass(prompt="Create your master password: ")
                re_enter_password = getpass.getpass(prompt="Re-enter your master password: ")

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            master_password_update(password, current_time)
            return True


def read_password_file():
    """
    Function employed in read the file which contains the password
    :return: list of dictionaries of password with titles
    """
    passwords = []
    try:
        with open(HOME + "/password.json", "r", encoding="utf-8") as file:
            for password in json.loads((file.read())):
                passwords.append(password)
    except FileNotFoundError:
        pass
    finally:
        return passwords


def update_passwords(passwords):
    """
    Function employed in writing the password to the file
    :param passwords: list of dictionaries of password with titles
    :return: None
    """
    with open(HOME + "/password.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(passwords, indent=4))


def copy2clip(text):
    """
    Function employed in copying password to clipboard
    :param text: txt that has to be copied to clipboard (str)
    :return: Copied text
    """
    pyperclip.copy(text)


def generate_password():
    """
    Function employed in generating random password
    :return: random password (str)
    """
    max_length = 12

    # all characters that are going to be used in password
    digits = list(string.digits)
    uppercase = list(string.ascii_uppercase)
    lowercase = list(string.ascii_lowercase)
    symbols = list(string.punctuation)

    combined_password = digits + uppercase + lowercase + symbols

    temp_password = random.choice(digits) + random.choice(uppercase) + random.choice(lowercase) + random.choice(symbols)

    temp_password_list = []
    for i in range(max_length - 4):
        temp_password = temp_password + random.choice(combined_password)  # taking a random character

        temp_password_list = array.array("u", temp_password)
        random.shuffle(temp_password_list)  # reshuffling the password

    return "".join(temp_password_list)  # returning the password

def delete_password(passwords, title):
    """
    Function employed in deleting a password
    :param passwords: list of passwords
    :param title: title of password to be deleted
    :return: None
    """
    index = 0
    found = False
    confirm = input("Do you really wanted to delete the password? (yes/no): ")
    if confirm.lower() == "yes":
        for password in passwords:
            if password.get("title").lower() == title.lower():
                found = True
                break
            index += 1

        if found:
            passwords.pop(index)
            update_passwords(passwords)
            print("Your password is successfully deleted. ")
        else:
            print("This password is not present. ")
    else:
        print("Delete operation aborted!")

        
def main():
    """
    Main function
    :return: None
    """
    passwords = read_password_file()
    args = sys.argv

    if len(args) == 7:  # adding the new password
        if args[1] == "add" and args[2] == "-title" and args[4] == "-username" and args[6] == "-generatepassword":
            if read_master_password_file():
                found = False
                for password in passwords:  # checking if password already exists
                    if args[3] == password.get("title"):
                        found = True
                        break

                if not found:
                    password = generate_password()  # generating new password
                    passwords.append({
                        "title": args[3],
                        "username": args[5],
                        "password": password
                    })

                    update_passwords(passwords)
                    sys.stdout.write("OK password created and copied to clipboard for next 30 seconds\n")
                    copy2clip(password)  # copying password to clipboard
                    time.sleep(30)
                    copy2clip("")  # removing the password from clipboard

                else:
                    sys.stdout.write("Password already exists for this title. \n")

            else:
                sys.stdout.write("Your master password is wrong\n")

        else:
            sys.stdout.write("Usage: python passman.py add -title instagram -username user123456 -generatepassword ("
                             "For generating new password)\n")

    elif len(args) == 4:
        if args[1] == "copy" and args[2] == "-title":
            title = args[3]
            if read_master_password_file():
                sys.stdout.write("Master password ok\n")
                found = False
                for password in passwords:
                    if password.get("title") == title:
                        username = password.get("username")
                        user_password = password.get("password")
                        sys.stdout.write("Username: {}|password copied to clipboard for next 30 seconds\n"
                                         "".format(username))
                        copy2clip(user_password)  # copying password to clipboard
                        time.sleep(30)
                        copy2clip("")  # removing the password from clipboard
                        found = True
                        break

                if not found:
                    sys.stdout.write("Your password exists for title: {}".format(title))

            else:
                sys.stdout.write("Your master password is wrong\n")

        else:
            sys.stdout.write("Usage: python passman.py copy -title instagram ("
                             "For copying password)\n")
    else:
        sys.stdout.write("Usage: python passman.py add -title instagram -username user123456 -generatepassword ("
                         "For generating new password)\n")
        sys.stdout.write("Usage: python passman.py copy -title instagram ("
                         "For copying password)\n")


if __name__ == '__main__':
    main()