import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('password_manager')


def check_array_exists(data_array):
    """
    Check if the given data array already exists in the passwords worksheet.
    
    """
    worksheet = SHEET.worksheet("passwords")
    column_a_values = worksheet.col_values(1)
    if data_array in column_a_values:
        return True
    return False



def get_passwords():
    """
    Get user data password information
    site, login, password
    """ 
    print("Please enter password data")
    print("Data consist of Site, Login and Password, separated by commas")
    print("Example: Facebook, mygmail@gmail.com, Pa$$word\n")

    data_string = input("Enter your data here: ")
    print(f"The password data is : {data_string}")

    data_array = data_string.split(',')
    if not check_array_exists(data_array[0]):  # Check only the value in column A (site)
        worksheet_to_update = SHEET.worksheet("passwords")
        worksheet_to_update.append_row(data_array) 
        print(f"Password added successfully\n")
    else:
        print("Password data already exists\n")
  

    

def main():
    """
    Run all program functions    
    """
    get_passwords()

# welcome text
print("Welcome to Password Manager")
main()  
    