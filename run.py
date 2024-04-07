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

def main():
    """
    Run all program functions    
    """
    get_passwords()

print("Welcome to Password Manager")
main()
    