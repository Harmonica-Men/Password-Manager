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
        
        # input("Press any key to continue...")
        
        worksheet_to_update.update_cell(row_index, 2, data_dict['login'])  # Update login value (column B)
        worksheet_to_update.update_cell(row_index, 3, data_dict['password'])  # Update password value (column C)

        print("Password data updated successfully")
    else:
        print("Invalid password data format. Please provide 'site', 'login', and 'password' keys.")

def list_all_entries():
    """
    List the first five entries in the passwords worksheet.
    """
    worksheet = SHEET.worksheet("passwords")
    data = worksheet.get_all_values()
    
    if len(data) > 1:
        # Convert data to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # Display the first five entries
        print("List of the first five entries:")
        print(df.head())
    else:
        print("No entries found in the passwords worksheet.")


def get_passwords():
    """
    Get user data password information
    site, login, password
    """
    while True:
        print("Please enter password data")
        print("Data consist of Site, Login, and Password, separated by commas")
        print("Example: Facebook, mygmail@gmail.com, Pa$$word\n")

        data_string = input("Enter your data here: ").lower()

        if not data_string:  # Check if the input string is empty
            print("No entry. Exiting...")
            break

        print(f"The password data is : {data_string}")

        data_array = data_string.split(',')
        if len(data_array) < 3:  # Check if login or password is missing
            print("Please provide all the required information (Site, Login, and Password)")
            continue

        data_dict = {'site': data_array[0], 'login': data_array[1], 'password': data_array[2]}

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
            worksheet_to_update.append_row(data_array)
            print(data_array)
            print(f"Password added successfully\n")

    
def main():
    """
    Run all program functions
    """
    print("Hello User")
    print("Welcome to Password Manager")
    get_passwords()
    list_all_entries()


main()
