# Import the gspread library for Google Sheets integration
import gspread
# Import the pandas library for data manipulation
import pandas as pd
# Import the string module for working with string constants
import string
# Import the random module for generating random values
import random
# Import the pyperclip module for accessing the clipboard
import pyperclip
# Import the os module for operating system-related functionality
import os

# Import the PyperclipException class for handling clipboard
from pyperclip import PyperclipException
# Import the Credentials class for authentication
from google.oauth2.service_account import Credentials
# Import the Fore class from colorama for colored text output,
# and init for initializing colorama
from colorama import Fore, init

# Initialize colorama with autoreset to reset colors after each print statement
init(autoreset=True)

global key  # Declare a global variable key
key = "KEY"  # Initialize the key variable with a value

# Define an exception message
EXCEPT_MSG = "Pyperclip could not find a copy/paste mechanism"
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
# Define the OAuth 2.0 scope for accessing Google Sheets and Google Drive
# Load credentials from a service account file
CREDS = Credentials.from_service_account_file('creds.json')
# Add the specified scopes to the credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# Authorize the gspread client with the scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Open the Google Sheets spreadsheet named 'password_manager'
SHEET = GSPREAD_CLIENT.open('password_manager')


def emptyblock():
    """
    Print an empty line.
    """
    print("\n")


def mylogo():
    os.system("clear")
    """
    Print the Password manager logo in ASCII art.
    """
    logo = """
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|P|a|s|s|w|o|r|d|-|M|a|n|a|g|e|r|  V1.00 DEMO
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    print(logo)


def Press_Enter():
    """
    Pause the program until ENTER is pressed.
    """
    emptyblock()
    input(f"Press Enter to continue ... \n")
    # os.system("clear")


def generate_random_password(length=15):
    """
    Generate a random password.
    """
    categories = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation
    ]  # Define character categories for password generation

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
    # Cut string in seperate variables (too long for PEP8)
    alpha0 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
    alpha1 = '!#$€%&()*+,-./:;<=>?@[]^_`{|}~'
    alphabet = alpha0 + alpha1
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
            print("Key Value Error:"+" Cannot divide by zero.")
            print("Return to menu ... ")
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
    # Access the "passwords" worksheet
    worksheet_to_update = SHEET.worksheet("passwords")
    # Get all values from Column A
    column_a_values = worksheet_to_update.col_values(1)
    # Check if the data array is in the values of Column A
    if data_array in column_a_values:
        # Return True if the data array exists
        return True
    # Return False if the data array does not exist
    return False


def update_password_data(data_dict):
    """
    Update existing password data in the passwords worksheet.
    """
    # Check if all required keys are present in the data dictionary
    if all(key in data_dict for key in ['site', 'login', 'password']):
        # Access the "passwords" worksheet
        worksheet_to_update = SHEET.worksheet("passwords")
        # Get all values from Column A
        column_a_values = worksheet_to_update.col_values(1)
        # Find the row index for the given site
        row_index = column_a_values.index(data_dict['site'].lower()) + 1
        # Update login value (column B)
        worksheet_to_update.update_cell(row_index, 2, data_dict['login'])
        # Update password value (column C)
        worksheet_to_update.update_cell(row_index, 3, data_dict['password'])
    else:
        # Print an empty block
        emptyblock()
        print("Invalid password data format.\n")
        print(" Please provide 'site', 'login'")
        print(", and 'password' keys")


def list_passwords(show_password):
    """
    List the specified number of entries in the passwords worksheet.
    If num_entries is None, all entries will be displayed.
    """
    # Access the "passwords" worksheet
    worksheet_to_update = SHEET.worksheet("passwords")
    # Get all values from the worksheet
    data = worksheet_to_update.get_all_values()
    # Convert the data into a list of arrays
    data_list = [row for row in data]
    # Check is there are any password in list
    
    #print("this data list:", data_list)
    if data_list == [[]]:
        line_exit("List is Empty")
        Press_Enter()
        return
        
    # Check if passwords should be displayed
    if show_password:
        # Initialize an empty list for decrypted data
        decrypted_data_list = []
        # Iterate through each row in the data
        for row in data:
            # Decrypt the password
            decrypted_password = vigenere_cipher(row[2], key, mode='decode')
            # Create a new row with decrypted password
            decrypted_row = [row[0], row[1], decrypted_password]
            # Add the decrypted row to the list
            decrypted_data_list.append(decrypted_row)
        # Update the data list with decrypted data
        data_list = decrypted_data_list
    # Initialize an empty list for new data dictionaries
    new_data_dict_list = []
    # Iterate through each row in the data list
    for i, row in enumerate(data_list):
        # Initialize a new data dictionary
        new_data_dict = {}
        # Add the row number to the dictionary
        new_data_dict["Row Number"] = i + 1
        # Add the site to the dictionary
        new_data_dict["Site"] = row[0]
        # Add the login to the dictionary
        new_data_dict["Login"] = row[1]
        # Add the password to the dictionary
        new_data_dict["Password"] = row[2]
        # Add the dictionary to the list
        new_data_dict_list.append(new_data_dict)
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(new_data_dict_list)
    # Reorder columns
    df = df[['Row Number', 'Site', 'Login', 'Password']]
    # Print an empty block
    emptyblock()
    # Print the DataFrame without headers and index
    print(df.iloc[0:].to_string(header=False, index=False))
    # Pause the program until ENTER is pressed
    Press_Enter()


def get_login():
    """
    Prompt the user to enter login or email.
    Returns the entered login if not empty.
    """
    while True:
        # Prompt the user to enter login or email
        print("Enter login or email ")
        # Get user input for login
        login = input(f"(press Enter for '{default_user}'): \n")
        # Check if login is empty
        if not login:
            emptyblock()
            # Print default login message
            print(Fore.GREEN + f"Using default login: {default_user}\n")
            # Return default user login
            return default_user
        else:
            # Return the entered login
            return login


def option_password():
    """
    Prompt the user to enter a password or auto-generate one.
    Returns the entered or generated password if it meets the requirements,
    otherwise prompts the user again.
    """
    while True:
        # Prompt the user to enter a password
        print("Enter password or ENTER ")
        # Get user input for password
        password = input("auto-generate a new password):")
        # Check if password is empty
        if not password:
            # Generate random password
            password = generate_random_password()
            # Print message for auto-generated password
            print(Fore.GREEN + "Using auto-generated password")
            # Return the auto-generated password
            return password
        # Check if password length is less than 6
        elif len(password) < 6:
            # Generate random password
            password = generate_random_password()
            # Print password length error message
            print(Fore.RED + "Password must be at least 6 characters long!")
            # Print message for auto-generated password
            print(Fore.RED + "Password is now auto-generated")
            # Return the auto-generated password
            return password
        else:
            # Return the entered password
            return password


def line_exit(info):
    """
    Print exit message and pause the program.
    """
    # Print an empty block
    emptyblock()
    # Print exit information in red color
    print(Fore.RED + info)
    # Print an empty block
    emptyblock()
    # Print message indicating no data processed and return to main menu
    print(Fore.RED + "No data processed ! ")
    print(Fore.RED + "Exiting ... Back to main menu ")
    Press_Enter()
    #os.system("clear")


def get_passwords():
    """
    Get user data password information: site, login, password
    """
    # Prompt user to create a new entry
    print("Create new entry ... ")
    # Prompt user to enter site or platform
    site = input("Enter new site or platform: ")
    # Check if the input string is empty
    # print("site: ", site)
    # breakpoint()
    if len(site) == 0:
        # Exit if input is empty
        # input("press enter to continue")
        line_exit("Empty input site or platform !!")
        Press_Enter()
        return
    # Check if site or platform string length exceeds 18 characters
    if len(site) > 18:
        # Print warning message
        print("Site or platform input string cannot")
        print(Fore.RED + " be greater than 18 characters!")
    # Check if site already exists
    if check_value_in_column_a(site.lower()):
        # Print warning message
        print(Fore.RED + "Site already exists !!")
        # Prompt user to change site
        print("Do you want to change the site?")
        print("Yes/No or press ENTER")
        # Get user choice
        choice = input("return Main menu ").lower()
        # Check if user wants to change site
        if choice == 'yes' or choice == 'y':
            # Get login information
            login = get_login()
            # Check if login is empty
            if login is None:
                # Exit if login is empty
                line_exit("The login input is empty ! ")
                return
            else:
                # Get password information
                password = option_password()
                # Initialize data dictionary
                data_dict = {}
                # Add site to data dictionary
                data_dict['site'] = site
                # Add login to data dictionary
                data_dict['login'] = login
                # Encrypt password
                encrypted = vigenere_cipher(password, key, mode="encode")
                # Add encrypted password to data dictionary
                data_dict['password'] = encrypted
                # Update password data
                update_password_data(data_dict)
            # Print empty block
            emptyblock()
            # Print success message
            print(Fore.GREEN + "Password added successfully")
            # Wait for user input
            Press_Enter()
            return
        # Check if user chooses not to change site
        elif choice == 'no' or choice == 'n':
            # Exit
            line_exit("")
            return
        else:
            # Handle invalid choice
            print(Fore.RED + "Invalid choice !!")
            # Print warning message
            print(Fore.RED + "No data processed ! ")
            print(Fore.RED + "Exiting ... Back to main menu ")
            Press_Enter()
            return
    else:
        # Get login information
        login = get_login()
        # Check if login is empty
        if login is None:
            # Exit if login is empty
            line_exit("The login input is empty !")
            return
        # Get password information
        password = option_password()
        # Check if password is empty
        if not password:
            # Exit if password is empty
            line_exit("Empty password input ...")
    # Create data dictionary
    data_dict = {'site': site, 'login': login, 'password': password}
    # Check if site already exists
    if check_value_in_column_a(data_dict['site']):
        # Print warning message
        print("Password data already exists.")
        # Prompt user to alter data
        choice = input(f" Do you want to alter it? (Yes/No): \n").lower()
        # Check if user wants to alter data
        if choice == 'yes' or choice == 'y':
            # Update password data
            update_password_data(data_dict)
        # Check if user chooses not to alter data
        elif choice == 'no' or choice == 'n':
            # Print the message
            print("No changes made to password data\n")
        # Handle invalid choice
        else:
            # Print warning message
            print(Fore.RED + "Invalid choice. Please enter 'Yes' or 'No'")
    else:
        # Access "passwords" worksheet
        worksheet_to_update = SHEET.worksheet("passwords")
        # Encrypt password
        encrypted_password = vigenere_cipher(password, key, mode="encode")
        # Create row data
        row_data = [site, login, encrypted_password]
        # Append row to worksheet
        worksheet_to_update.append_row(row_data)
        # Print empty block
        emptyblock()
        # Print success message
        print(Fore.GREEN + "Password added successfully")
        # Wait for user input
        Press_Enter()
        return


def password_visible() -> bool:
    """
    Prompt the user for a Yes or No answer and return a boolean value.
    If the input is neither Yes nor No,
    return False to indicate going back to the main menu.
    """
    # Prompt user for visibility
    print("Do you wish to make passwords visible during password listing?")
    # Get user choice
    choice = input(f"Press Yes/No or ENTER: ").lower()
    # If the user presses Enter without input
    if not choice:
        return False
    elif choice == 'yes' or choice == 'y':  # If user chooses Yes
        return True
    elif choice == 'no' or choice == 'n':  # If user chooses No
        return False
    # Handle invalid input
    else:
        # Print empty block
        emptyblock()
        print("Invalid Input , hide passwords ")
        Press_Enter()


def copy_password_entry(index_number):
    """
    Copy the password entry from the specified index in the DataFrame.
    """
    # Access "passwords" worksheet
    worksheet_to_update = SHEET.worksheet("passwords")
    # Get all values from the worksheet
    data = worksheet_to_update.get_all_values()
    # Get the number of rows in the worksheet
    max_row = len(data)
    # Get values of the first row
    row1_values = worksheet_to_update.row_values(1)
    # Check if the first row is empty
    if not row1_values:
        # Exit function if there is no password list
        line_exit("There is no password list to copy from")
        return
    # Check if the index is within the range of rows
    if int(index_number) <= max_row:
        # Convert the data into a list of arrays
        data_list = [row for row in data]
        # Decrypt the passwords using a Vigenère cipher
        for row in data_list:
            row[2] = vigenere_cipher(row[2], key, mode='decode')
        # Get the password entry at the specified index
        password_entry = data_list[int(index_number)][2]
        try:
            # Copy the password entry to the clipboard
            pyperclip.copy(password_entry)
        except PyperclipException as e:
            # Exit function if copying fails
            line_exit("Failed to copy password entry to clipboard")
            return
    else:
        emptyblock()
        print(Fore.RED + f"Your index {index_number} exceeds the maximum")
        print(Fore.RED + " of rows {max_row} in this worksheet")
        # Exit function if the index exceeds the maximum number of rows
        line_exit("")
        return
    emptyblock()
    print(Fore.GREEN + "Password is copied into the clipboard ")
    # Wait for user input
    Press_Enter()


def check_if_number(input_str):
    """
    Check if the input is a number
    """
    # Check if input is of type int or float
    if isinstance(input_str, (int, float)):
        # Return True if input is a number
        return True
    # Check if input consists of digits only
    if input_str.isdigit():
        # Return True if input is a number
        return True
    # Return False if input is not a number
    return False


def check_worksheet_value0():
    """
    Checks if the worksheet has any values.
    Returns True if the worksheet is not empty, False otherwise.
    """
    # Access "passwords" worksheet
    worksheet_to_update = SHEET.worksheet("passwords")
    # Get all values from the worksheet
    data = worksheet_to_update.get_all_values()
    # Get the number of rows in the worksheet
    zero_value = len(data)
    # Check if there are no values in the worksheet
    if not zero_value:
        # Set iszero to False if there are no values
        iszero = False
    else:
        # Set iszero to True if there are values
        iszero = True
    # Print the number of rows in the worksheet
    print("Zero value:", zero_value)
    # Print whether the worksheet is empty or not
    print("Is zero:", iszero)
    # Return True if the worksheet is not empty, False otherwise
    return iszero


def delete_password_entry(index_number):
    """
    Delete the password entry from the specified index in the DataFrame.
    """
    # Access "passwords" worksheet
    worksheet_to_update = SHEET.worksheet("passwords")
    # Get all values from the worksheet
    data = worksheet_to_update.get_all_values()
    # Get values of the first row
    row1_values = worksheet_to_update.row_values(1)
    # Get the number of rows in the worksheet
    max_row = len(data)
    # Check if the index number is within the range of rows
    if int(index_number) <= max_row:
        # Get values of the first row
        row1_values = worksheet_to_update.row_values(1)
        # Check if there are no values in the first row
        if not row1_values:
            # Exit if there are no values
            line_exit("There are no password entries")
        else:
            # Delete the row at the specified index
            worksheet_to_update.delete_rows(index_number)
            # Print empty block
            emptyblock()
            # Print success message
            print(Fore.GREEN + "Password entry at")
            print(Fore.GREEN + f"index {index_number} is deleted")
            # Wait for user input
            Press_Enter()
    else:
        # Check if the number of rows is less than or equal to 1
        if int(max_row) <= 1:
            # Exit if there are no password entries
            line_exit("There are no password entries")
        else:
            # Exit if index is out of range
            split_string0 = "Index exceeds the maximum number"
            split_string1 = " of rows in password list"
            split_string = split_string0 + split_string1
            # Split string to big for PEP8
            line_exit(split_string)
            
        # End function execution
        return


def menu_option_1():
    """
    Function to handle menu option 1: Create new entry
    """
    # Display the logo
    mylogo()
    # Display menu option
    print("Menu Option 1\n")
    # Call function to create a new password entry
    get_passwords()


def menu_option_2():
    """
    Function to handle menu option 2: List passwords
    """
    # Display the logo
    mylogo()
    # Display menu option
    print("Menu Option 2\n")
    # Inform user about listing passwords
    print("List passwords ... ")
    # Call function to list passwords
    list_passwords(password_visible())


def menu_option_3():
    """
    Update the key for password encryption/decryption.
    """
    # Display the logo
    mylogo()
    # Declare key as global
    global key
    # Store the old key
    old_key = key
    # Display menu option
    print("Menu option 3\n")
    # Inform user about changing the cipher key
    print("Change cipher key ... ")
    while True:
        # Display the old key
        print("The old key: " + Fore.CYAN + key)
        # Prompt user for the new key
        key = input("Enter the new: ")
        # Check if the new key is empty or too long
        if len(key) == 0 or len(key) > 8:
            # Restore the old key
            key = old_key
            if len(key) > 8:
                # Inform user about key length limit
                line_exit("cipher key is too long (max 8 characters)")
                return
            else:
                # Inform user about empty key
                line_exit("cipher key is empty")
                return
        else:
            break
    # Write empty print statement
    emptyblock()
    # Inform user about successful key update
    print(Fore.GREEN + "Cipher Key updated successfully")
    # Prompt user to press Enter
    Press_Enter()


def menu_option_4():
    """
    Function to handle menu option 0: delete record in password list
    """
    # Display the logo
    mylogo()
    # Display menu option
    print("Menu option 0\n")
    # Inform user about deleting a password by index
    print("Delete password by index ... ")
    # Prompt user for the record number to delete
    index_number = input("number of record to be deleted?: ")
    # Check if the input is empty
    if not index_number:
        # Inform user about empty input
        line_exit("You entered nothing")
        Press_Enter()
    else:
        # Check if the input is a number
        if check_if_number(index_number):
            # Call function to delete password entry
            delete_password_entry(int(index_number))
            #print(Fore.GREEN + f"password entry {index_number} succesfully deleted from list")
            #Press_Enter()
        else:
            # Inform user about invalid input
            line_exit("Invalid input")
            Press_Enter()


def menu_option_5():
    """
    Function to handle menu option 5: Change default user login
    """
    # Access the global variable
    global default_user
    # Store the old default user login
    old_user = default_user
    # Display the logo
    mylogo()
    # Display menu option
    print("Menu option 5 \n")
    # Inform user about changing default user login
    print("Change default user login ... ")
    while True:
        # Display current default user login
        print(f"The default user login: {default_user}\n")
        # Prompt user for new default user login
        default_user = input("Enter new user login: ")
        # Check if the input is empty
        if len(default_user) <= 0:
            # Restore the old default user login
            default_user = old_user
            # Inform user about empty input
            line_exit("You entered nothing")
            break
        else:
            # Check if the input exceeds 25 characters
            if len(default_user) >= 25:
                # Restore the old default user login
                default_user = old_user
                print(Fore.RED + "default user login must be smaller")
                print(Fore.RED + " then 25 characters long.")
                print(Fore.RED + "No data processed! ")
                print(Fore.RED + "Exiting ... Back to main menu ")
                Press_Enter()
                break
            else:
                # Write empty print statements
                emptyblock()
                # Message password is added successfully
                print(Fore.GREEN + "Default password added successfully")
                Press_Enter()
                break


def menu_option_6(update_bool):
    """
    Function to handle menu option 6: Change master password
    """
    # Clear the console screen
    os.system("clear")
    # Display the logo
    mylogo()
    # Loop until a condition is met
    while True:
        # Check if update_bool is True
        if update_bool:
            # Display message for bypass option
            print("Press ENTER to bypass (DEMO)")
            # Prompt for master password
            master_password = input("Enter master password: ")
        else:
            # Display message for changing master password
            print("Menu option 6\n")
            print("Change master password ... ")
            # Prompt for new master password
            master_password = input("Enter new master password: ")
        # Check if the input is empty
        if len(master_password) <= 0:
            # Display an empty block
            emptyblock()
            # Inform about continuing with demo version
            print(Fore.GREEN + "DEMO version allowed to continue ")
            # Wait for Enter key press
            Press_Enter()
            # Return True indicating demo version continuation
            return True
        else:
            # Check if the input exceeds 20 characters or is smaller then 3 characters
            if len(master_password) >= 20 or len(master_password) <= 3:
                print(Fore.RED + "Enter master password must be ")
                print(Fore.RED + "greater then 3 and smaller then 20")
                print(Fore.RED + "characters long.")
                emptyblock()
                print(Fore.RED + "No data processed!")
                print(Fore.RED + "Exiting ... Back to main menu ")
                Press_Enter()
                # Break the loop
                break
            else:
                # Access the master password worksheet
                worksheet_to_update = SHEET.worksheet("masterpassword")
                # Get the stored master password
                password = worksheet_to_update.cell(2, 1).value
                # Decode the stored password
                password = vigenere_cipher(password, key, mode="decode")
                # Check if entered master password matches the stored one
                if master_password == password:
                    # If in update mode
                    if update_bool:
                        # Return True indicating successful verification
                        return True
                    # If not in update mode
                    else:
                        print(Fore.RED + "Master password is the same. ")
                        print(Fore.RED + "Nothing updated. ")
                        # Wait for Enter key press
                        Press_Enter()
                        # Return False indicating no update
                        return False
                else:
                    # If in update mode
                    if update_bool:
                        print(Fore.RED + "Master password incorrect.")
                        emptyblock()
                        print(Fore.RED + "Exiting ... ")
                        # Wait for Enter key press
                        Press_Enter()
                        # Return False indicating failed verification
                        return False
                    # If not in update mode
                    else:
                        # switch string because line to long for PEP8
                        mbstr = master_password
                        # Encode the new master password
                        mystr = vigenere_cipher(mbstr, key, mode="encode")
                        # Access the master password worksheet
                        worksheet_to_update = SHEET.worksheet("masterpassword")
                        # Update the master password
                        worksheet_to_update.update_cell(2, 1, mystr)
                        # Display an empty block
                        emptyblock()
                        # Inform about successful update
                        print(Fore.GREEN + "Master password is updated ")
                        # Wait for Enter key press
                        Press_Enter()
                        # Return False indicating successful update
                        return False


def main():
    """
    Run all program functions
    """
    # Declare key as a global variable
    global key
    # Declare default_user as a global variable
    global default_user
    # Set default_user to a test email address
    default_user = "Harmonica_men"
    # Set the initial key for encryption/decryption
    key = "PaLenTir"
    # Call menu_option_6 function with True argument to indicate initial run
    menu_loop = menu_option_6(True)
    # Define the menu options
    menu = """
*** Menu ***
    
    1. update / create a new entry
    2. list passwords
    3. set cipher key
    4. delete a record in password list
    5. change default user login
    6. change master password
    7. quit

Please enter your choice (1-7): """
    # If the menu loop is True (indicating successful setup)
    # start the menu loop
    if menu_loop:
        while True:
            # Display the program logo
            mylogo()
            # Prompt the user for a menu choice
            user_choice = input(f"{menu} \n")
            # Based on the user's choice,
            # call the corresponding menu option function
            if user_choice == '1':
                # Clear the console screen
                # os.system("clear")
                # Call the function to handle menu option 1
                menu_option_1()                
            elif user_choice == '2':
                # Clear the console screen
                # os.system("clear")
                # Call the function to handle menu option 2
                menu_option_2()
            elif user_choice == '3':
                # Clear the console screen
                # os.system("clear")
                # Call the function to handle menu option 3
                menu_option_3()
            elif user_choice == '4':
                # Clear the console screen
                # os.system("clear")
                # Call the function to handle menu option 0
                menu_option_4()
            elif user_choice == '5':
                # Clear the console screen
                # os.system("clear")
                # Call the function to handle menu option 5
                menu_option_5()
            elif user_choice == '6':
                # Clear the console screen
                # os.system("clear")
                # Call the function to handle menu option 6
                menu_loop == menu_option_6(False)
            elif user_choice == '7':
                # Clear the console screen
                # os.system("clear")
                # Copy an empty string to clear the clipboard
                print("Thank you for using Password Manager")
                print("Have a nice day ...")
                break
            else:
                # Display an empty block
                print(user_choice)
                emptyblock()
                # Message the input choice is not valid
                print(Fore.RED + "Invalid choice.")
                print(Fore.RED + "Please enter a number between 1 and 7")
                # Wait for Enter key press
                Press_Enter()
    else:
        # Clear the console screen if menu loop setup failed
        os.system("clear")


# Main program
if __name__ == "__main__":
    # Call the main function if the script is executed directly
    main()