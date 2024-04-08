import gspread
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

    Args:
        data_dict (dict): A dictionary containing the password data.
    """
    if all(key in data_dict for key in ['site', 'login', 'password']):  # Check if all required keys are present
        worksheet = SHEET.worksheet("passwords")
        column_a_values = worksheet.col_values(1)
        input("Press any key to continue...")
        row_index = column_a_values.index(data_dict['site'].lower()) + 1
        worksheet.update('B' + str(row_index), data_dict['login'])  # Update login value
        worksheet.update('C' + str(row_index), data_dict['password'])  # Update password value
        print("Password data updated successfully")
    else:
        print("Invalid password data format. Please provide 'site', 'login', and 'password' keys.")


def get_passwords():
    """
    Get user data password information
    site, login, password
    """
    print("Please enter password data")
    print("Data consist of Site, Login and Password, separated by commas")
    print("Example: Facebook, mygmail@gmail.com, Pa$$word\n")

    data_string = input("Enter your data here: ").lower()
    print(f"The password data is : {data_string}")

    data_array = data_string.split(',')
    if check_value_in_column_a(data_array[0]):  # Check if value exists in column A (site)
        choice = input("Password data already exists. Do you want to alter it? (Yes/No): ").lower()
        if choice == 'yes':
            update_password_data(data_array)
        elif choice == 'no':
            print("No changes made to password data")
        else:
            print("Invalid choice. Please enter 'Yes' or 'No'")
    else:
        worksheet_to_update = SHEET.worksheet("passwords")
        worksheet_to_update.append_row(data_array)
        print(f"Password added successfully\n")

    
def main():
    """
    Run all program functions
    """
    print("Hello User")
    print("Welcome to Password Manager")
    get_passwords()


main()
