import gspread
import pandas as pd
import string
import random

from google.oauth2.service_account import Credentials

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
    Generate a random password of the specified length.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

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
    #print(f"/n")
    #print (data_dict)
    
    if all(key in data_dict for key in ['site', 'login', 'password']):  # Check if all required keys are present
        worksheet = SHEET.worksheet("passwords")
        column_a_values = worksheet.col_values(1)
        
        row_index = column_a_values.index(data_dict['site'].lower()) + 1

        worksheet_to_update = SHEET.worksheet("passwords")
                
        worksheet_to_update.update_cell(row_index, 2, data_dict['login'])  # Update login value (column B)
        worksheet_to_update.update_cell(row_index, 3, data_dict['password'])  # Update password value (column C)

        print("Password data updated successfully")
    else:
        print("Invalid password data format. Please provide 'site', 'login', and 'password' keys.")


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
    if show_password:
        pass
    else:
        for row in data_list:
            row[2] = vigenere_cipher(row[2], key, mode='decode')  # decrypt the third variable 

    # Convert the list of arrays into a list of dictionaries
    new_data_dict_list = [{"Site": row[0], "Login": row[1], "Password": row[2]} for row in data_list]

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(new_data_dict_list)

    # Print the DataFrame without headers and from the second row 
    if num_entries:
        print(df.iloc[1:].head(num_entries).to_string(header=False, index=False))
    else:
        print(df.iloc[1:].to_string(header=False, index=False))

    
def get_passwords():
    """
    Get user data password information: site, login, password
    """
    
    print(f"Please enter password data\n")

    while True:
        site = input("Enter site or platform: ")
        if not site:  # Check if the input string is empty
            print("Empty input site")
            return  # Break out of the function if site is empty

        # Check if site already exists
        if check_value_in_column_a(site.lower()):
            print("Site already exists")
            return

        while True:
            login = input("Enter login or email: ")
            if not login:  # Check if the input string is empty
                print("Empty input login")
                return  # Break out of the function if login is empty
            break  # Break out of the inner while loop if login is provided

        while True:
            password_option = input("Do you want to auto-generate a password? (Yes/No): ").lower()
            if password_option == 'yes' or password_option == 'y':
                password = generate_random_password()  # Generate random password
                break
            elif password_option == 'no' or password_option == 'n':
                password = input("Enter password: ")
                break
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")

        if not password:
            print("Empty input password")
            return  # Break out of the function if password is empty
        break  # Break out of the outer while loop after both site, login, and password are provided

    data_dict = {'site': site, 'login': login, 'password': password}

    if check_value_in_column_a(data_dict['site']):  # Check if value exists in column A (site)
        choice = input("Password data already exists. Do you want to alter it? (Yes/No): ").lower()
        if choice == 'yes' or choice == 'y':
            update_password_data(data_dict)
        elif choice == 'no' or choice == 'n':
            print(f"No changes made to password data\n")
        else:
            print("Invalid choice. Please enter 'Yes' or 'No'")
    else:
        worksheet_to_update = SHEET.worksheet("passwords")
        worksheet_to_update.append_row([site, login, vigenere_cipher(password,key,mode='encode')])
        print(f"Password added successfully\n")

def password_visible():
    """
    Prompt the user for a Yes or No answer and return a boolean value.
    If the input is neither Yes nor No, return False to indicate going back to the main menu. 
    """
        
    while True:
        user_input = input("Do wish to make password visible during password listing ? 'Yes' or 'no'")
        if user_input == 'yes' or user_input == 'y':
            return True
        elif user_input == 'no' or user_input == 'n':
            return False
        else:
            return False
            print("Invalid input. Please enter 'Yes' or 'No'.")
            # user_input = False
       
def main():
    """
    Run all program functions
    """
    
    global key 
    
    key = "KEY"

    menu = """


 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |P|a|s|s|w|o|r|d|-|M|a|n|a|g|e|r|
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


    
*** Menu ***

    1. create new entry
    2. list passwords
    3. set decipher key
    4. set password complexity
    5. hide / unhide password

    6. quit

    
    Please enter your choice (1-5): """

    while True:
        user_choice = input(menu)

        match user_choice:
            case '1':
                print("Creating new entry...")
                get_passwords()

            case '2':
                # Ask user for number of entries to display
                print("Listing passwords...")
                
                num_entries = input("Enter the number of entries to display (leave empty to display all): ")
    
                if num_entries.strip():  # Check if input is not empty
                    try:
                        num_entries = int(num_entries)
                    except ValueError:
                        print(f"Invalid input. Please enter a valid number.\n")
                        return
                else:
                    num_entries = None  # Show all entries if input is empty
                    
                list_passwords(num_entries,password_visible())
                
            case '3':
                key = input("Enter the key for password: ")
                print(f"Decipher key set to: {key}")
                
            case '4':
                print("Setting password complexity...")

            
            case '5':
                print(f"TY for using Password Manager\n")
                print(f"Bye bye ...\n")
                break

            case _:
                print("Invalid choice. Please enter a number between 1 and 5.")
    
    
    
# Main program    
    

if __name__ == "__main__":
    main()