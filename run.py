import gspread
import pandas as pd

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

def caesar_cipher(text, shift):
    """
    Apply Caesar Cipher to the given text by shifting all alphabet letters to the right by the specified shift value.
    
    Args:
        text (str): The text to be encrypted.
        shift (int): The number of characters to shift each alphabet letter.
    
    Returns:
        str: The encrypted text.
    """
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            # Determine if it's uppercase or lowercase
            if char.isupper():
                encrypted_char = chr((ord(char) - 65 + shift) % 26 + 65)  # Shift uppercase letters
            else:
                encrypted_char = chr((ord(char) - 97 + shift) % 26 + 97)  # Shift lowercase letters
        else:
            encrypted_char = char  # Keep non-alphabet characters unchanged
        encrypted_text += encrypted_char
    return encrypted_text


def check_value_in_column_a(data_array):
    """
    Check if the given data array already exists in the passwords worksheet.
    Only for column A

    """
    worksheet = SHEET.worksheet("passwords")
    column_a_values = worksheet.col_values(1)  # Check Column A
    if data_array in column_a_values:
        return True
    return False


def update_password_data(data_dict):
    """
    Update existing password data in the passwords worksheet.
    """
    print(f"/n")
    print (data_dict)
    
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

def list_all_entries(num_entries=None):
    """
    List the specified number of entries in the passwords worksheet.
    If num_entries is None, all entries will be displayed.
    """
    worksheet = SHEET.worksheet("passwords")
    data = worksheet.get_all_values()
    
    if len(data) > 1:
        # Convert data to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # Display the specified number of entries or all entries if None
        if num_entries is None:
            print("List of all entries:")
            print(df)
        else:
            print(f"List of the first {num_entries} entries:")
            print(df.head(num_entries))
    else:
        print("No entries found in the passwords worksheet.")

def get_passwords():
    """
    Get user data password information
    site, login, password
    """

    # data_dict = {'site': site, 'login': login, 'password': password}

    while True:
        print(f"Please enter password data/n")
               
        password = "Pa$$word123" #dummy password

        while True:
            site = input("Enter site or platform: ")
            if not site:  # Check if the input string is empty
                print("Empty input site")
                return  # Break out of the function if site is empty

            while True:
                login = input("Enter login or email: ")
                if not login:  # Check if the input string is empty
                    print("Empty input login")
                    return  # Break out of the function if login is empty

                break  # Break out of the inner while loop if login is provided

            break  # Break out of the outer while loop after both site and login are provided

        if not login or not site:  # Check if either login or site is empty
            print("No data entered. Exiting...")
            return  # Break out of the function if either login or site is empty

        # password = input(f"enter the password: ")

        print(site)
        print(login)
        print(password)
        print(f"encrypted : {caesar_cipher(password,5)}")

        input("PRESS ANY KEY TO CONTINUE .... ")

        data_dict = {'site': site, 'login': login, 'password': caesar_cipher(password,5)}

        print(f"Site: {site}")
        print(f"Login: {login}")
        print(f"Password: {caesar_cipher(password,5)}")

        if check_value_in_column_a(data_dict['site']):  # Check if value exists in column A (site)
            choice = input("Password data already exists. Do you want to alter it? (Yes/No): ").lower()
            if choice == 'yes':
                update_password_data(data_dict)
            elif choice == 'no':
                print("No changes made to password data")
            else:
                print("Invalid choice. Please enter 'Yes' or 'No'")
        else:
            worksheet_to_update = SHEET.worksheet("passwords")
            worksheet_to_update.append_row([site, login, caesar_cipher(password,5)])
            print("Password added successfully\n")

    
def main():
    """
    Run all program functions
    """
    print("Hello User")
    print("Welcome to Password Manager\n")
    get_passwords()
    
    # Ask user for number of entries to display
    num_entries = input("Enter the number of entries to display (leave empty to display all): ")
    
    if num_entries.strip():  # Check if input is not empty
        try:
            num_entries = int(num_entries)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return
    else:
        num_entries = None  # Show all entries if input is empty
        
    list_all_entries(num_entries)


main()
