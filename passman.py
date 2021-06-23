import array
import csv
import datetime
import getpass
import json
import pathlib
import random
import string
import sys
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
    :return: True or False (boolean)
    -> True: If master password is typed in correctly by the user or last access is less than 24 hours
    -> False: If master password is typed in incorrectly by the user
    """
    master_password = {}
    found = False # boolean variable if master password file was found or not
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
                if password == master_password["password"]: # check if entered master password is correct
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # get current time & initialize it to variable current_time
                    master_password_update(password, current_time) # overwrite last access with current time
                    return True
                else:
                    return False
            else:
                return True

        else:  # if file is not found then create the file
            password = getpass.getpass(prompt="Create your master password: ")
            re_enter_password = getpass.getpass(prompt="Re-enter your master password: ")

            while password != re_enter_password:  # ask for password until password1 matches password2
                password = getpass.getpass(prompt="Create your master password: ")
                re_enter_password = getpass.getpass(prompt="Re-enter your master password: ")

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # get current time & initialize it to variable current_time
            master_password_update(password, current_time) # overwrite last access with current time
            return True


def read_password_file():
    """
    Function employed to read the file which contains the password
    :return: list of passwords with titles
    """
    passwords = [] # declaring list variable passwords
    try:
        with open(HOME + "/password.json", "r", encoding="utf-8") as file:
            for password in json.loads((file.read())): # for-loop to get all the passwords
                passwords.append(password) # writing all the password data from the file to the list variable
    except FileNotFoundError:
        pass # continuing with the code - file doesn't exist if there haven't been created any passwords yet
    finally:
        return passwords


def update_passwords(passwords):
    """
    Function employed in writing the password to the file
    :param passwords: list of password with titles
    :return: None
    """
    with open(HOME + "/password.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(passwords, indent=4)) # writing the password to the file


def copy2clip(text):
    """
    Function employed in copying password to clipboard
    :param text: text that has to be copied to clipboard (str)
    :return: Copied text
    """
    pyperclip.copy(text)


def generate_password(length=12, case="", symbol=""):
    """
    Function employed in generating random password with user defined parameters
    :param length: user can select the length of the password; default is 12
    :param case: user can choose between lower- and uppercase; default is mixed lower- and uppercase
    :param symbol: user can choose to have symbols in password or not
    :return: random password (str)
    """
    max_length = length

    # all options that are going to be used for generating the password
    digits = list(string.digits)
    uppercase = list(string.ascii_uppercase)
    lowercase = list(string.ascii_lowercase)
    symbols = list(string.punctuation)

    if case.lower() == "l": # password with only lowercase 
        if symbol == "no": # password without symbols
            combined_password = digits + lowercase
            temp_password = random.choice(digits) + random.choice(lowercase)
        else: # password with symbols
            combined_password = digits + lowercase + symbols
            temp_password = random.choice(digits) + random.choice(lowercase) + random.choice(symbols)

    elif case.lower() == "u": # password with only uppercase
        if symbol == "no": # password without symbols
            combined_password = digits + uppercase
            temp_password = random.choice(digits) + random.choice(uppercase)
        else: # password with symbols
            combined_password = digits + uppercase + symbols
            temp_password = random.choice(digits) + random.choice(uppercase) + random.choice(symbols)

    else: # password with lower- and uppercase (default option)
        if symbol == "no": # password with symbols
            combined_password = digits + uppercase + lowercase
            temp_password = random.choice(digits) + random.choice(uppercase) + random.choice(lowercase)
        else: # password without symbols
            combined_password = digits + uppercase + lowercase + symbols
            temp_password = random.choice(digits) + random.choice(uppercase) + random.choice(lowercase) + random.choice(symbols)

    temp_password_list = [] # declaring list variable
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
    index = 0 # counter to keep track of the position in the list while looping 
    found = False
    confirm = input("Do you really wanted to delete the password? (yes/no): ")
    if confirm.lower() == "yes":
        for password in passwords: # for-loop to check if title exists 
            if password.get("title").lower() == title.lower():
                found = True
                break
            index += 1

        if found: # if title was found then delete entry
            passwords.pop(index)
            update_passwords(passwords)
            print("Your password is successfully deleted. ")
        else:
            print("This password is not present. ")
    else:
        print("Delete operation aborted!")


def add_password(passwords, **kwargs):
    """
    Function employed in adding the a new password
    :param passwords: list of passwords
    :param kwargs: additional arguments - title & username
    :return: None
    """
    # initializing variables with data of parameters
    title = kwargs.get("title")
    username = kwargs.get("username")

    length = (input("Length of password (default = 12): "))
    cases = input("'u' for only uppercase | 'l' for only lowercases (default = mixed): ")
    symbol = input("Symbols? 'yes' | 'no' (default: yes): ")
    url = input("URL (default = empty): ")
    
    if length == "": # default length (12)
        password = generate_password(case=cases, symbol=symbol)  # generating new password
    else: # length defined by user
        password = generate_password(int(length), case=cases, symbol=symbol)
    
    # adding new password data to passwords list
    passwords.append({ 
        "title": title,
        "username": username,
        "password": password,
        "url": url
    })

    update_passwords(passwords) # writing the password data to the file
    sys.stdout.write("OK password created and copied to clipboard for next 30 seconds\n")
    copy2clip(password)  # copying password to clipboard
    time.sleep(30)
    copy2clip("")  # removing the password from clipboard


def change_password(passwords, title):
    """
    Function employed in changing the password
    :param passwords: list of passwords
    :param title: title whose password is going to be changed
    :return: None
    """
    index = 0 # counter to keep track of the position in the list while looping 
    found = False # boolean if title was found or not
    for password in passwords: # for-loop to check if title exists 
        if password.get("title").lower() == title.lower():
            found = True
            break
        index += 1

    if found:
        passwords[index].update({"password": generate_password()}) # updating passwords list with new password
        update_passwords(passwords) # writing the password to the file
        print("Password has been changed successfully & copied to Clipboard for next 30 seconds")
        password_new = passwords[index].get("password")
        copy2clip(password_new)  # copying password to clipboard
        time.sleep(30)
        copy2clip("")  # removing the password from clipboard

    else:
        print("Title: {} not found. ".format(title))


def export_password(passwords, file_name):
    """
    Function employed in exporting data to CSV files
    :param passwords: list of passwords
    :param file_name: name of file
    :return: None
    """
    rows = [["title", "username", "password", "url"]] # initializing list with names of columns
    for password in passwords: # adding the password data to rows list
        rows.append([password.get("title"), password.get("username"), password.get("password"), password.get("url")])
    file = open(file_name, "w", encoding="utf-8") # creating file (name defined by user)
    print(rows) # output of password data
    
    # writing the password data to the file in csv format
    writer = csv.writer(file) 
    writer.writerows(rows)
    file.close()


def update_master():
    """
    Function employed in updating Master-Password
    :return: None
    """
    master_password = {}

    with open(HOME + "/master_password.json", "r", encoding="utf-8") as file:  # opening master password file
        file_data = json.loads(file.read())
        master_password["password"] = file_data.get("password")

        password = getpass.getpass(prompt="Enter current Master-Password: ") # check current master password
        if password == master_password["password"]: # if master password is correct 
            password_new = getpass.getpass(prompt="Create your Master-Password: ")
            re_enter_password = getpass.getpass(prompt="Re-enter your Master-Password: ")

            while password_new != re_enter_password:  # ask for password until password1 matches password2
                print("\nTyped in passwords do not match - Please try again:")
                password_new = getpass.getpass(prompt="Create your Master-Password: ")
                re_enter_password = getpass.getpass(prompt="Re-enter your Master-Password: ")

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            master_password_update(password_new, current_time) # get current time & initialize it to variable current_time
            print("Master-Password successfully updated.") # overwrite last access with current time

        else: 
            print("Entered Master-Password is wrong")

def copy_password(passwords, title): 

    found = False
    for password in passwords: # for-loop to check if title exists
        if password.get("title") == title:
            username = password.get("username")
            user_password = password.get("password")

            sys.stdout.write("Username: {} | Password copied to Clipboard for next 30 seconds\n".format(username))
            
            copy2clip(user_password)  # copying password to clipboard
            time.sleep(30)
            copy2clip("")  # removing the password from clipboard
            found = True
            break

    if not found:
        sys.stdout.write("Your password does not exist for title: {}".format(title))

def help(): 
    """
    Output of available functions
    """
    print("\n### HELP - USE FOLLOWING COMMANDS ###\n\nGenerating new password:\npython passman.py add -title instagram -username user123456 -generatepassword\n")
    print("Copying password to clipboard:\npython passman.py copy -title instagram\n")
    print("Deleting password:\npython passman.py delete -title instagram\n")
    print("Exporting passwords to CSV:\npython passman.py export -filename export.csv\n")
    print("Changing password:\npython passman.py change -title instagram\n")
    print("Changing Master-Password:\npython passman.py master -update\n")
    print("Help:\npython passman.py help")

def main():
    """
    Main function
    :return: None
    """
    
    passwords = read_password_file()
    args = sys.argv   # ability to work with command line arguments

    if len(args) == 7:  # adding the new password
        if args[1] == "add" and args[2] == "-title" and args[4] == "-username" and args[6] == "-generatepassword":
            if read_master_password_file():
                found = False
                for password in passwords:  # checking if title already exists
                    if args[3] == password.get("title"):
                        found = True
                        break

                if not found:
                    add_password(passwords, title=args[3], username=args[5])

                else:
                    sys.stdout.write("Password already exists for this title. \n")

            else:
                sys.stdout.write("Your Master-Password is wrong\n")

        else:
            sys.stdout.write("Usage: python passman.py add -title instagram -username user123456 -generatepassword ("
                             "For generating new password)\n")

    elif len(args) == 4 and args[1] == "delete" and args[2] == "-title": # deleting password
        if read_master_password_file():
            title = args[3]
            delete_password(passwords, title)
        else:
            sys.stdout.write("Your master password is wrong\n")

    elif len(args) == 4 and args[1] == "change" and args[2] == "-title": # changing password
        if read_master_password_file():
            title = args[3]
            change_password(passwords, title)
        else:
            sys.stdout.write("Your master password is wrong\n")

    elif len(args) == 4 and args[1] == "export" and args[2] == "-filename": # exporting passwords to CSV
        if read_master_password_file():
            export_password(passwords, args[3])
        else:
            sys.stdout.write("Your master password is wrong\n")

    elif len(args) == 3 and args[1] == "master" and args[2] == "-update": # updating master password
        update_master()

    elif len(args) == 4 and args[1] == "copy" and args[2] == "-title": # copying password
        if read_master_password_file(): 
            title = args[3]
            copy_password(passwords, title)
        else: 
            sys.stdout.write("Your Master-Password is wrong\n")

    elif len(args) == 2 and args[1] == "help": # help function
        help()

    else: 
        help()

if __name__ == '__main__':
    main()
