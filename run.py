import gspread
import pandas as pd
import string
import random
import pyperclip
import os

from pyperclip import PyperclipException
from google.oauth2.service_account import Credentials
from colorama import Fore, init

init(autoreset=True)

global key
key = "KEY"

EXCEPT_MSG = "Pyperclip could not find a copy/paste mechanism"
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('password_manager')


def emptyblock():
    """
    print a empty line
    """
    print("\n")


def mylogo():
    """
    print the Password manager logo in ascii-art
    """
    logo = """        
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|P|a|s|s|w|o|r|d|-|M|a|n|a|g|e|r|  V1.00 DEMO
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    print(logo)


def Press_Enter():
    """
    Pauze the program, until pressed ENTER
    """
    emptyblock()
    input(f"Press Enter to continue ... \n")
    os.system("clear")


def generate_random_password(length=15):
    """
    Generate a random password
    """
    categories = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation
    ]

    password = []
    selected_categories = random.sample(categories, k=3)
    # Select at least one character from each selected category
    for category in selected_categories:
        password.append(random.choice(category))
    # Select remaining characters randomly
    for _ in range(length - 3):
        category = random.choice(categories)
        password.append(random.choice(category))
    # Shuffle the password to ensure randomness
    random.shuffle(password)
    return ''.join(password)


def vigenere_cipher(text, key, mode='encode'):
    """
    Apply Vigenère Cipher to the given text using the provided key.
    """
    if mode not in ['encode', 'decode']:
        raise ValueError("Invalid mode. Mode must be 'encode' or 'decode'.")
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    
    #text = text.upper()
    #key = key.upper()
    # Initialize the result string
    result = ''
    # Set the appropriate shift direction based on the mode
    if mode == 'encode':
        shift_factor = 1
    else:
        shift_factor = -1
    # Iterate through each character in the text
    for i, char in enumerate(text):
        # Skip characters not present in the alphabet
        if char not in alphabet:
            result += char
            continue
        try:
            key_char = key[i % len(key)]
        except ZeroDivisionError:
            print(f"Key Value Error:"+" Cannot divide by zero.\n")
            print(f"Return to menu ... \n")
            break
        key_char = key[i % len(key)]
        key_pos = alphabet.index(key_char)
        # Apply the Vigenère Cipher shift
        char_pos = alphabet.index(char)
        shifted_pos = (char_pos + shift_factor * key_pos) % len(alphabet)
        # Append the shifted character to the result string
        result += alphabet[shifted_pos]
    return result


def check_value_in_column_a(data_array):
    """
    Check if the given data array already exists in the passwords worksheet.
    Only for column A
    """
    worksheet_to_update = SHEET.worksheet("passwords")
    column_a_values = worksheet_to_update.col_values(1)  # Check Column A
    if data_array in column_a_values:
        return True
    return False


def update_password_data(data_dict):
    """
    Update existing password data in the passwords worksheet.
    """
    if all(key in data_dict for key in ['site', 'login', 'password']):
        # Check if all required keys are present
        worksheet = SHEET.worksheet("passwords")
        column_a_values = worksheet.col_values(1)
        row_index = column_a_values.index(data_dict['site'].lower()) + 1
        worksheet_to_update = SHEET.worksheet("passwords")
        worksheet_to_update.update_cell(row_index, 2, data_dict['login'])
        # Update login value (column B)
        worksheet_to_update.update_cell(row_index, 3, data_dict['password'])
        # Update password value (column C)
    else:
        emptyblock()
        print(f"Invalid password data format.\n")
        print(f" Please provide 'site', 'login'")
        print(", and 'password' keys")


def list_passwords(show_password):
    """
    List the specified number of entries in the passwords worksheet.
    If num_entries is None, all entries will be displayed.
    """
    worksheet_to_update = SHEET.worksheet("passwords")
    data = worksheet_to_update.get_all_values()
    # Convert the data into a list of arrays
    data_list = [row for row in data]
    # Decrypt the passwords using a Vigenère cipher
    if show_password:
        decrypted_data_list = []
        for row in data:
            decrypted_password = vigenere_cipher(row[2], key, mode='decode')
            decrypted_row = [row[0], row[1], decrypted_password]
            decrypted_data_list.append(decrypted_row)
        data_list = decrypted_data_list
    new_data_dict_list = []
    for i, row in enumerate(data_list):
        new_data_dict = {}  
        new_data_dict["Row Number"] = i + 1 
        new_data_dict["Site"] = row[0]
        new_data_dict["Login"] = row[1]
        new_data_dict["Password"] = row[2]
        new_data_dict_list.append(new_data_dict)
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(new_data_dict_list)
    # Reorder columns to have 'Row Number' as the first column
    df = df[['Row Number', 'Site', 'Login', 'Password']]
    emptyblock()
    print(df.iloc[0:].to_string(header=False, index=False))
    Press_Enter()


def get_login():
    """
    Prompt the user to enter login or email.
    Returns the entered login if not empty.
    """
    while True:
        print("Enter login or email ")
        login = input(f"(press Enter for '{default_user}'): \n")
        if not login:
            emptyblock()
            print(Fore.GREEN + f"Using default login: {default_user}\n")
            return default_user
        else:
            return login


def option_password():
    """
    Prompt the user to enter a password or auto-generate one.
    Returns the entered or generated password if it meets the requirements,
    otherwise prompts the user again.
    """
    while True:
        print(f"Enter password or ENTER\n")
        password = input(f"auto-generate a new password): \n")
        if not password:
            password = generate_random_password()  # Generate random password
            print(Fore.GREEN + "Using auto-generated password")
            return password
        elif len(password) < 6:
            password = generate_random_password()  # Generate random password
            print(Fore.RED + f"Password must be at least 6 characters long!\n")
            print(Fore.RED + "Password is now auto-generated")
            return password
        else:
            return password
        
def line_exit(info):
    emptyblock()
    print(Fore.RED + info)
    emptyblock()
    print(Fore.RED + f"No data processed ! \n")
    print(Fore.RED + f"Exiting ... Back to main menu \n")
    Press_Enter()


def get_passwords():
    """
    Get user data password information: site, login, password
    """
    print(f"Create new entery ... \n")
    while True:
        site = input(f"Enter new site or platform: ")
        if not site:  # Check if the input string is empty
            line_exit("Empty input site or platfrom !!")
            return
        if len(site) > 18:
            print(f"Site or platform input string cannot")
            print(Fore.RED + f" be greater than 18 characters!\n")
            continue
        if check_value_in_column_a(site.lower()):
            print(Fore.RED + f"Site already exists !!\n")
            print("Do you want to change the site?")
            print("Yes/No or press ENTER")
            choice = input(f"return Main menu \n").lower()
            if choice == 'yes' or choice == 'y':
                login = get_login()
                if login is None:
                    line_exit("The login input is empty ! ")
                    return
                else:
                    password = option_password()
                    data_dict = {}
                    data_dict['site'] = site
                    data_dict['login'] = login
                    encrypted = vigenere_cipher(password, key, mode="encode")
                    data_dict['password'] = encrypted
                    update_password_data(data_dict)
                emptyblock()
                print(Fore.GREEN + f"Password added successfully\n")
                Press_Enter()
                return
            elif choice == 'no' or choice == 'n':
                line_exit("")
                return
            else:
                print(Fore.RED + f"Invalid choice !!\n")
                print(Fore.RED + f"No data processed ! \n")
                print(Fore.RED + f"Exiting ... Back to main menu \n")
                Press_Enter()
                return
        else:
            login = get_login()
            if login is None:
                line_exit("The login input is empty !")
                return
            password = option_password()
            if not password:
                line_exit("Empty password input ...")
                
        data_dict = {'site': site, 'login': login, 'password': password}
        if check_value_in_column_a(data_dict['site']):
            print(f"Password data already exists.")
            choice = input(f" Do you want to alter it? (Yes/No): \n").lower()
            if choice == 'yes' or choice == 'y':
                update_password_data(data_dict)
            elif choice == 'no' or choice == 'n':
                print(f"No changes made to password data\n")
            else:
                print(Fore.RED + "Invalid choice. Please enter 'Yes' or 'No'")
        else:
            worksheet_to_update = SHEET.worksheet("passwords")
            encrypted_password = vigenere_cipher(password, key, mode="encode")
            row_data = [site, login, encrypted_password]
            worksheet_to_update.append_row(row_data)
            emptyblock()
            print(Fore.GREEN + f"Password added successfully\n")
            Press_Enter()
            return #end loop


def password_visible() -> bool:
    """
    Prompt the user for a Yes or No answer and return a boolean value.
    If the input is neither Yes nor No,
    return False to indicate going back to the main menu.
    """
    print(f"Do you wish to make passwords visible during password listing?\n")
    while True:
        choice = input(f"Press Yes/No or ENTER: ").lower()
        if not choice:  # If the user presses Enter without input
            return False
        elif choice == 'yes' or choice == 'y':
            return True
        elif choice == 'no' or choice == 'n':
            return False
        else:
            emptyblock()
            print(f"Invalid input\n")


def copy_password_entry(index_number):
    """
    Copy the password entry from the specified index in the DataFrame.
    """
    worksheet_to_update = SHEET.worksheet("passwords")
    data = worksheet_to_update.get_all_values()
    max_row = len(data)
    row1_values = worksheet_to_update.row_values(1)
    
    if not row1_values:
        print("debug1")
        line_exit("There is password list to copy from")
        return  
    
    if int(index_number) <= max_row:
        # Convert the data into a list of arrays
        data_list = [row for row in data]
        # Decrypt the passwords using a Vigenère cipher
        for row in data_list:
            row[2] = vigenere_cipher(row[2], key, mode='decode')
        password_entry = data_list[int(index_number)][2]
        try:
            pyperclip.copy(password_entry)
        except PyperclipException as e:
            line_exit("Failed to copy password entry to clipboard")
            return
    else:
        emptyblock()
        print(Fore.RED + "Your index exceed the maximum" 
            + "of rows {max_row} in this")
        line_exit("")
        return
    emptyblock()
    print(Fore.GREEN + f"Password is copied into the clipboard \n")
    Press_Enter()


def check_if_number(input_str):
    # Check if the input is a number
    if isinstance(input_str, (int, float)):
        return True
    if input_str.isdigit():
        return True
    return False

def check_worksheet_value0():
    """
    Checks if the worksheet has any values.
    Returns True if the worksheet is not empty, False otherwise.
    """
    worksheet_to_update = SHEET.worksheet("passwords")
    data = worksheet_to_update.get_all_values()
    zero_value = len(data)
    
    if not zero_value:
        iszero = False
    else:
        iszero = True
    
    print("Zero value:", zero_value)
    print("Is zero:", iszero)
    
    return iszero


def delete_password_entry(index_number):
    """
    Delete the password entry from the specified index in the DataFrame.
    """

    worksheet_to_update = SHEET.worksheet("passwords")
    data = worksheet_to_update.get_all_values()
    row1_values = worksheet_to_update.row_values(1)

    max_row = len(data)

    if int(index_number) <= max_row:
        row1_values = worksheet_to_update.row_values(1)
        if not row1_values:
                line_exit("there are no password enteries")
        else:
            worksheet_to_update.delete_rows(index_number)
            emptyblock()
            print(Fore.GREEN + f"Password entry index {index_number} is deleted")
            Press_Enter()
    else:
        if int(max_row) <= 1:
            line_exit("there are no password enteries")
        else:
            line_exit("index exceed the maximum of rows in password list")
        return


def menu_option_0():
    """
    Function to handle menu option 0: delete record in password list
    """
    mylogo()
    print(f"Menu option 0\n")
    print(f"Delete password by index ... \n")
    index_number = input(f"number of record to be deleted?: ")
    if not index_number:
        line_exit("You entered nothing")
    else:
        if check_if_number(index_number):
            delete_password_entry(int(index_number))
        else:
            line_exit("Invalid input")


def menu_option_1():
    """
    Function to handle menu option 1: Create new entry
    """
    mylogo()
    print(f"Menu Option 1 \n")
    get_passwords()


def menu_option_2():
    """
    Function to handle menu option 2: List passwords
    """
    mylogo()
    print(f"Menu Option 2\n")
    print(f"List passwords ...\n")
    list_passwords(password_visible())


def menu_option_3():
    """
    Update the key for password encryption/decryption.
    """
    mylogo()
    global key  # Declare key as global
    old_key = key
    print(f"Menu option 3\n")
    print(f"Change cipher key ... \n")
    while True:
        print(f"The old key: " + Fore.CYAN + key)
        key = input(f"Enter the new: ")
        if len(key) == 0 or len(key) > 8:
            key = old_key
            if len(key) > 8:
                line_exit("cipher key is to long (max 8 charaters)")
                return
            else:
                line_exit("cipher key is empty")
                return
        else:
            break
    emptyblock()
    print(Fore.GREEN + f"Cipher Key updated successfully\n")
    Press_Enter()


def menu_option_4():
    """
    Copy/paste password by entery number
    """
    mylogo()
    print(f"Menu option 4\n")
    print(f"Copy/paste password ...\n")
    index_number = input(f"number copy/paste into clipboard?: \n")
    if not index_number:
        line_exit("You entered nothing")
    else:
        if int(index_number) == 0:
            line_exit("Invalid input")
        else:
            if check_if_number(index_number):
                copy_password_entry(int(index_number))
            else:
                line_exit("Invalid input")


def menu_option_5():
    global default_user
    old_user = default_user
    mylogo()
    print(f"Menu option 5\n")
    print(f"Change default user login ...\n")
    while True:
        print(f"The default user login: {default_user}\n")
        default_user = input(f"Enter new user login: ")
        if len(default_user) <= 0:
            default_user = old_user
            line_exit("You entered nothing")
            break
        else:
            if len(default_user) >= 25:
                default_user = old_user
                print(Fore.RED + "default user login must be smaller")
                print(Fore.RED + f" then 25 characters long.\n")
                print(Fore.RED + f"No data processed! \n")
                print(Fore.RED + f"Exiting ... Back to main menu \n")
                Press_Enter()
                break
            else:
                emptyblock()
                print(Fore.GREEN + f"Default password added successfully\n")
                Press_Enter()
                break


def menu_option_6(update_bool):
    """
    menu option 6 has dual functionality to enter master password before 
    using it in the menu option loop
    """
    os.system("clear")
    mylogo()
    while True:
        if update_bool:
            print(f"Press ENTER to bypass (DEMO)\n")
            master_password = input("Enter master password: ")
        else:
            print(f"Change master password ... \n")
            master_password = input(f"Enter new master password: ")
        if len(master_password) <= 0:
            emptyblock()
            print(Fore.GREEN + f"DEMO version allowed to continue \n")
            Press_Enter()
            return True
        else:
            if len(master_password) >= 20:
                print(Fore.RED + "Enter master password less")
                print(Fore.RED + " then 20 characters long.\n")
                print(Fore.RED + f"No data processed! \n")
                print(Fore.RED + f"Exiting ... Back to main menu \n")
                break
            else:
                worksheet_to_update = SHEET.worksheet("masterpassword")
                password = worksheet_to_update.cell(2, 1).value
                password = vigenere_cipher(password, key, mode="decode")
                if master_password == password:
                    if update_bool:
                        return True
                    else:
                        print(Fore.RED + "Master password is the same. ")
                        print(Fore.RED + "Nothing updated. ")
                        Press_Enter()
                        return False
                else:
                    if update_bool:
                        print(Fore.RED + f"Master password incorrect.\n")
                        print(Fore.RED + f"Exiting ... \n")
                        Press_Enter()
                        return False
                    else:                                              
                        mystr = vigenere_cipher(master_password, key, mode="encode")
                        worksheet_to_update = SHEET.worksheet("masterpassword")
                        worksheet_to_update.update_cell(2, 1, mystr)
                        emptyblock()
                        print(Fore.GREEN + "Master password is updated ")
                        Press_Enter()
                        return False


def main():
    """
    Run all program functions
    """
    global key
    global default_user
    default_user = "TestUser@gmail.com"
    key = "KEY"
    menu_loop = menu_option_6(True)
    menu = """
*** Menu ***

    0. delete a record in password list
    1. update / create a new entry
    2. list passwords
    3. set cipher key
    4. copy / paste password
    5. change default user login
    6. change master password
    7. quit

Please enter your choice (0-7): """
    if menu_loop:
        
        while True:
            mylogo()
            user_choice = input(f"{menu} \n")
            if user_choice == '0':
                os.system("clear")
                menu_option_0()
            elif user_choice == '1':
                os.system("clear")
                menu_option_1()
            elif user_choice == '2':
                os.system("clear")
                menu_option_2()
            elif user_choice == '3':
                os.system("clear")
                menu_option_3()
            elif user_choice == '4':
                os.system("clear")
                menu_option_4()
            elif user_choice == '5':
                os.system("clear")
                menu_option_5()
            elif user_choice == '6':
                os.system("clear")
                menu_loop == menu_option_6(False)
            elif user_choice == '7':
                os.system("clear")
                # Copy an empty string to clear the clipboard
                print(f"Thank you for using Password Manager\n")
                print(f"Have a nica day ...\n")
                try:
                    pyperclip.copy('')
                except PyperclipException as e:
                    pass
                    #line_exit("Failed to copy password entry to clipboard")
                break
            else:
                emptyblock()
                print(Fore.RED + "Invalid choice.")
                print(Fore.RED + f" Please enter a number between 0 and 7.\n")
                Press_Enter()
    else:
        os.system("clear")


# Main program
if __name__ == "__main__":
    main()
