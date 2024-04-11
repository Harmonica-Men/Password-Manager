import gspread
import pandas as pd
import string
import random
import pyperclip
import os

from google.oauth2.service_account import Credentials
from colorama import Fore, Style, init

init(autoreset=True)

global key 
    
key = "KEY"

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('password_manager')



def generate_random_password(length=12):
    """
    Generate a random password of the specified length meeting complexity requirements.
    """
    categories = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation
    ]

    password = []

    # Ensure the password contains characters from at least three of the five categories
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
    
    # Define the alphabet including both uppercase letters and symbolic characters
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    # Convert both text and key to uppercase
    text = text.upper()
    key = key.upper()
    
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
                
        # Determine the position of the current key character
        try: 
            key_char = key[i % len(key)] 
        except ZeroDivisionError: 
            print(f"Key Value Error: Cannot divide by zero.\n") 
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
       
    if all(key in data_dict for key in ['site', 'login', 'password']):  # Check if all required keys are present
        worksheet = SHEET.worksheet("passwords")
        column_a_values = worksheet.col_values(1)
        row_index = column_a_values.index(data_dict['site'].lower()) + 1
        worksheet_to_update = SHEET.worksheet("passwords")
        worksheet_to_update.update_cell(row_index, 2, data_dict['login'])  # Update login value (column B)
        worksheet_to_update.update_cell(row_index, 3, data_dict['password'])  # Update password value (column C)
        # emptyblock()
        # print(Fore.GREEN + f"Password data updated successfully\n")
        # emptyblock()
        # os.system("clear")
    else:
        emptyblock()
        print(f"Invalid password data format. Please provide 'site', 'login', and 'password' keys.\n")
        emptyblock

# Print emtpy block of lines
def emptyblock():
    print("\n" * 2)


def list_passwords(num_entries=None, show_password=bool):
    """
    List the specified number of entries in the passwords worksheet.
    If num_entries is None, all entries will be displayed.
    """
    worksheet_to_update = SHEET.worksheet("passwords")
    data = worksheet_to_update.get_all_values()

    # Convert the data into a list of arrays
    data_list = [row for row in data]

    # Decrypt the passwords using a Vigenère cipher
    if not show_password:
        data_list = [[row[0], row[1], vigenere_cipher(row[2], key, mode='decode')] for row in data_list]

   
    # Convert the list of arrays into a list of dictionaries
    new_data_dict_list = [{"Row Number": i, "Site": row[0], "Login": row[1], "Password": row[2]} for i, row in enumerate(data_list)]

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(new_data_dict_list)

    # Reorder columns to have 'Row Number' as the first column
    df = df[['Row Number', 'Site', 'Login', 'Password']]

    # Print the DataFrame without headers and from the second row 
    if num_entries:
        print(df.iloc[1:].head(num_entries).to_string(header=False, index=False))
    else:
        print(df.iloc[1:].to_string(header=False, index=False))
    
def get_login():
    """
    Prompt the user to enter login or email.
    Returns the entered login if not empty.
    """
    while True:
        login = input(f"Enter login or email (press Enter for '{default_user}'): ")
        if not login:  # Check if the input string is empty
            print(Fore.GREEN + f"Using default login: {default_user}\n")
            return default_user
        else:
            return login  # Return the entered login if not empty


def option_password():

    password = input("Enter password: (press ENTER to auto-generate a new password) : ")

    if not password:
        password = generate_random_password()  # Generate random password          
        print(Fore.GREEN + f"Using auto-generated password\n")  
        return password
    else:
        return password        

def get_passwords():
    """
    Get user data password information: site, login, password
    """

    while True:
        site = input("Enter site or platform: ")
        if not site:  # Check if the input string is empty
            print(Fore.RED + "Empty input site or platfrom !!")
            print(Fore.RED + f"No data processed! \n")
            print(Fore.RED + f"Exiting ... Back to main menu \n")
            emptyblock
            input(f"Press Enter to continue ... \n")
            os.system("clear")
            return  # Break out of the function if site is empty

        # Check if site already exists
        if check_value_in_column_a(site.lower()):
            print(Fore.RED + f"Site already exists !!\n")
            print("Do you want to change the site?")
            choice = input(f"Yes/No or press ENTER to return\n").lower()
            
            # print(Style.RESET_ALL)
            if choice == 'yes' or choice == 'y':
                login = get_login()
                if login == None:
                    print(Fore.RED + f"The login input is empty ! \n")
                    print(Fore.RED + f"No data processed ! \n")
                    print(Fore.RED + f"Exiting ... Back to main menu \n")
                    emptyblock
                    input(f"Press Enter to continue ... \n")
                    os.system("clear")
                    return
                else:
                    password = option_password()        

                # print(password)
                data_dict = {'site': site, 'login': login, 'password': vigenere_cipher(password,key,mode="encode")}
                update_password_data(data_dict)

                emptyblock()
                print(Fore.GREEN + f"Password added successfully\n")
                emptyblock
                input(f"Press Enter to continue ... \n")
                os.system("clear")

                return  
            
            elif choice == 'no' or choice == 'n':
                print(Fore.RED + f"No data processed ! \n")
                print(Fore.RED + f"Exiting ... Back to main menu \n")
                emptyblock
                input(f"Press Enter to continue ... \n")
                os.system("clear")
                return  
            else:
                # print(Fore.RED + f"Invalid choice. Please enter " + Fore.CYAN + "(Yes\No)")
                continue  
        else:
            # Prompt for login using the get_login function
            login = get_login()  
            # print("Login ", login)
            if login == None:
                print(Fore.RED + f"The login input is empty !\n")
                print(Fore.RED + f"No data processed ! \n")
                print(Fore.RED + f"Exiting ... Back to main menu \n")
                emptyblock
                input(f"Press Enter to continue ... \n")
                os.system("clear")
                return  
            
            
            password = option_password()
            if not password:
                print(Fore.RED + f"Empty password input ... \n")
                print(Fore.RED + f"No data processed ! \n")
                print(Fore.RED + f"Exiting ... Back to main menu \n")
                emptyblock
                input(f"Press Enter to continue ... \n")
                os.system("clear")
                
                return  # Break out of the function if password is empty
            break  # Break out of the outer while loop after both site, login, and password are provided

    data_dict = {'site': site, 'login': login, 'password': password}

    if check_value_in_column_a(data_dict['site']):  # Check if value exists in column A (site)
        choice = input("Password data already exists. Do you want to alter it? (Yes/No): ").lower()
        if choice == 'yes' or choice == 'y' or choice == 'Y':
            update_password_data(data_dict)
        elif choice == 'no' or choice == 'n' or choice == 'N':
            print(f"No changes made to password data\n")
        else:
            print(Fore.RED + "Invalid choice. Please enter 'Yes' or 'No'")
    else:
        worksheet_to_update = SHEET.worksheet("passwords")
        worksheet_to_update.append_row([site, login, vigenere_cipher(password,key,mode="encode")])
        emptyblock()
        print(Fore.GREEN + f"Password added successfully\n")
        emptyblock
        input(f"Press Enter to continue ... \n")
        # print(Style.RESET_ALL)
        os.system("clear")

def password_visible():
    """
    Prompt the user for a Yes or No answer and return a boolean value.
    If the input is neither Yes nor No, return False to indicate going back to the main menu. 
    """
        
    while True:
        user_input = input("Do wish to make password visible during password listing ? 'Yes' or 'no'")
        if user_input == 'no' or user_input == 'N' or user_input == 'n':
            return True
        elif user_input == 'yes' or user_input == 'Y' or user_input == 'y':
            return False
        else:
            print(Fore.RED + "Invalid input. Please enter 'Yes' or 'No'.")
            return True

def copy_password_entry(index_number):
    """
    Copy the password entry from the specified index in the DataFrame.
    """

    worksheet_to_update = SHEET.worksheet("passwords")
    data = worksheet_to_update.get_all_values()
    max_row = len(data)

    if int(index_number) <= max_row:

        # Convert the data into a list of arrays
        data_list = [row for row in data]

        # Decrypt the passwords using a Vigenère cipher
        for row in data_list:
            row[2] = vigenere_cipher(row[2], key, mode='decode')  # decrypt the third variable 

        password_entry = data_list[int(index_number)][2]
        pyperclip.copy(password_entry)
    else:
        print(Fore.RED + f"Your index exceed the maximum of rows {max_row} in this\n")


def menu_option_1():
    """
    Function to handle menu option 1: Create new entry
    """

    M_option1 = """
    
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |P|a|s|s|w|o|r|d|-|M|a|n|a|g|e|r|
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
*** Menu Option 1 - Creating a new entry... 
"""
    print(M_option1)
    get_passwords()



def menu_option_2():
    """
    Function to handle menu option 2: List passwords
    """
    
    print(f"Menu Option 2\n")
    print(f"\n")
    print(f"List passwords ...\n")
    print(f"\n")
    emptyblock()
    
    num_entries = input(f"Enter the number of entries to display " + Fore.CYAN + " (leave empty to display all): ")

    if num_entries.strip():  # Check if input is not empty
        try:
            num_entries = int(num_entries)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid number.")
            return
    else:
        num_entries = None  # Show all entries if input is empty
        
    list_passwords(num_entries, password_visible())
   

def menu_option_3():
    """
    Update the key for password encryption/decryption.
    """

    global key  # Declare key as global

    old_key = key
  
    print(f"Menu option 3\n")
    print(f"Change cipher key ...\n")

    while True:
        key = input(f"The old key: {key} \nEnter new key: ")
        if key == "":
            break  
        elif len(key) < 3 or len(key) > 8:
            key = old_key
            print(Fore.RED + f"Key must be between 3 and 8 characters long.\n")
            print(Fore.RED + f"No data processed! \n")
            print(Fore.RED + f"Exiting ... Back to main menu \n")
            emptyblock
            input(f"Press Enter to continue ... \n")
            os.system("clear")
            return
        else:
            break  

def menu_option_4():
    """
    Copy/paste password by entery number
    """
    
    print(f"Menu option 4\n")
    print(f"Copy/paste password ...\n")   
    index_number = input(f"Enter password index number copy/paste into clipboard? : ")
    copy_password_entry(index_number)

def menu_option_5():
    global default_user
  
    print(f"Menu option 5\n")
    print(f"Change default user login ...\n")

    while True:
        default_user = input(f"The default user login: {default_user} \nEnter new user login : ")
        if default_user == "":
            print(Fore.RED + f"No data processed! \n")
            print(Fore.RED + f"Exiting ... Back to main menu \n")
            emptyblock
            input(f"Press Enter to continue ... \n")
            os.system("clear")
            break 
        elif len(default_user) > 12:
            print(Fore.RED + f"default user login must be smaller then 12 characters long.\n")
            print(Fore.RED + f"No data processed! \n")
            print(Fore.RED + f"Exiting ... Back to main menu \n")
            emptyblock
            input(f"Press Enter to continue ... \n")
            os.system("clear")
            return
        else:
            break 
           
def main():
    """
    Run all program functions
    """
    global key 
    global default_user

    default_user = "testuser1"
    key = "KEY"
    
    os.system("clear")
    menu = """

    
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |P|a|s|s|w|o|r|d|-|M|a|n|a|g|e|r|
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
*** Menu ***

    1. create a new entry
    2. list passwords
    3. set cipher key
    4. copy / paste password 
    5. change default user login
    6. quit
    
    Please enter your choice (1-6): """

    while True:
        user_choice = input(menu)

        match user_choice:
            # add or create new enteries
            case '1':
                os.system("clear")
                menu_option_1() 
                
            # list hidden passwords
            case '2':
                os.system("clear")
                menu_option_2() 
                
            # update key
            case '3':
                os.system("clear")
                menu_option_3() 
                                
            # copy / paste password
            case '4':
                os.system("clear")
                menu_option_4() 

            # set default_user
            case '5':
                os.system("clear")
                menu_option_5()
                            
            case '6':
                os.system("clear")
                print(f"TY for using Password Manager\n")
                print(f"Bye bye ...\n")
                break

            case _:      
                emptyblock()                    
                print(Fore.RED + f"Invalid choice. Please enter a number between 1 and 5.\n")
                emptyblock()
                input(f"Press Enter to continue ... \n")
                os.system("clear")
                
    
# Main program    
if __name__ == "__main__":
    main()