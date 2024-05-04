![demo-gif](assets/images/Password-Manager-Demo.gif)

## Index - Table of Contents

- [Password Manager](#password-manager)
- [Important Security Warning](#important-security-warning)

- [UX](#ux)

  - [Site Goals](#site-goals)
  - [User Stories](#user-stories)

- [A Step By Step Guide](#a-step-by-step-guide)

  - [Step 1 DEMO version](#step-1-demo)
  - [Step 2 RUN PROGRAM](#step-2-run-program)
  - [Step 3 Enter Master Password](#Step-3-Enter-Master-Password)
  - [Step 4 Main Options](#Step-4-Main-Options)
    - [Menu Option 1](#Menu-option-1)
      Update / Create a new entry
    - [Menu Option 2](#Menu-Option-2)
      List passwords
    - [Menu Option 3](#Menu-Option-3)
      Set Cipher Key
    - [Menu Option 4](#Menu-Option-4)
      Delete a record in password list
    - [Menu Option 5](#Menu-Option-5)
      Change user default password
    - [Menu Option 6](#Menu-Option-6)
      Change master password
    - [Menu Option 7](#Menu-Option-7)
      Quit (Step 5)

- [Technology Used](#technologies)

- [Testing](#testing)

  - [Validator Testing](#validator-testing)
  - [Manual Testing](#manual-testing)
  - [Fixed Bugs](#fixed-bugs)

- [Deployment](#deployment)

- [Credits](#credits)

- [ Acknowledgements](#acknowledgements)

##

# Password-Manager

As a user you are concerned about the security of your online accounts.
You want a Password Manager program!!
So that you can keep track, securely store and manage all your passwords.
If you have internet access you can access your passwords.

## Important Security Warning

This open source version of Password-Manager is suitable for **testing** and **educational** purposes only.

This is a demonstration program where fictional accounts and associate passwords,
are stored in this case on the google cloud.

It's essential to understand you **NEVER** store passwords into the cloud!! Because,
basically put yourself in a very uncomfortable position to expose of your privacy. Because the cloud is not **YOUR** intellectual property.

# UX

## Site Goals

To access and manage all your accounts & password over the internet via SSH terminal as a End-To-End Encryption
to your by passing your Firewall to your local domain on a Server that function as a Password-Manager. (for example a Raspberry Pi)

## User Stories

As a user I want:

- To be able to update, create or delete account and password enteries.
- To lists passwords and give a choice to the user obscure them from view or show the password explicitly by request.
- To be able to set a Cipher-Key, this is a handy feature to add a extra level of complexity to obsucre your passwords.
- To set up a default user login, makes the UX more user friendly
- To always be able to change the 'master password' to access the password-manager.
- **note** There was a **copy/paste** password clipboard feature available that I need to removed because it was not possible to integrate that
  in Heroku cloud environment.

As the administrator I want:

- access the file that's stored the content of the accounts and passwords.
- the passwords itself are encrypted.

# A Step By Step Guide

## Step 1 Demo

The live DEMO version of Password-Manager is online running on Heroku, [Here](https://terminal-password-manager-2fad20bf8063.herokuapp.com/) the repo is located [here](https://github.com/Harmonica-Men/Password-Manager)

## Step 2 RUN PROGRAM

![scr02](assets/images/password-manager-scr02.png)
_ Enter a valid password to access the program (you can always be changed afterwards)  
 _ Press Enter to bypass (DEMO version)

## Step 3 Enter Master Password

![scr03](assets/images/password-manager-scr03.png)

## Step 4 Main Options

![scr04](assets/images/password-manager-scr04.png)

### Menu option 1

**Update / Create a New Entry**

- Two choices:
  1. Press Enter to return to main menu
  2. Enter new site or platfrom
- Enter a new site: CodeInstitute (example)
- Enter login credentials, again two choices
  1. Press Enter for the default login
  2. Enter your credentials
- Enter password, again two choices
  1. Press Enter to auto-generated new random password
  2. Enter your own password
- Password added successfully

![scr05](assets/images/password-manager-scr05.png)

### Menu Option 2

**List passwords**

![scr06](assets/images/password-manager-scr06.png)

- Two choices whether or not you wish the password to be visible during the listing?
      1. user choice is : No or Enter
  ![scr07](assets/images/password-manager-scr07.png)

- all accounts and passwords entries are chown whit encrypted passwords.
      2. user choice is : Yes
  ![scr08](assets/images/password-manager-scr08.png)
  all accounts and passwords entries are now chown whit there true context. (de-ciphered password)

### Menu Option 3

**Change Cipher Key**

- This allow the user to change how password are encrypted into the google spreadsheet. The main advantage is to add a extra level of complexity how your password are stored or displayed.
- Inorder to ativie this a 'Caeser cipher' is used as basic principle.
  by shifting the alphabet in a number of letters left or right, the password can be obsured. However instead of using a decimal places to shift in this program a cipher key is used. This methode is also know as the 'Vigenère cipher'.
  For additional information about the Vigenère cipher check this link: [Here](https://https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher/)

![scr09](assets/images/password-manager-scr09.png)

- **note** When Enter a blank cipher key, the key is not changed and the user return back to the Main Menu

### Menu Option 4

**Delete a Record In Password Manager List**

- This allow the user to delete a record from the password list
- By enter a record index number the record is deleted.
- When Enter a blank index number the user goes back to the Main Menu
  ![scr10](assets/images/password-manager-scr10.png)

### Menu Option 5

**Change Default User Login**

- This give the possiblity to enter a pre-determent user into password manager when a new account - password entry gonna been entered.
- Here also two choices, enter a new user login or
- When the user leaves the login input field empty the user returns back to Main Menu.
  ![scr11](assets/images/password-manager-scr11.png)

### Menu Option 6

**Change The Master Password**
![password-manager-scr12.png](assets%2Fimages%2Fpassword-manager-scr12.png)

- Every **$door$** has a key and in this case a extra level protection is been added, there is a master password to remember to access the main program, this is in fact the only password to be remembered.
- Here are also two choices, enter a new master password or  
- Leave the master password entry empty to go back to the main menu.
- Do not forget your using the DEMO version of password manager allowing you to bypass the master password confirmation on startup. But the master password is actually changed.

### Menu Option 7

**Quit**

- This option is to quit the Password-Manager
  ![scr13](assets/images/password-manager-scr13.png)

## Technologies

- Heroku
  - Used to deploy and host the application
- Python
  - Code used to create the application
- Visual Code
  - Visual Studio Code (VS Code) was developed by Microsoft. It is a free, open-source code editor designed for writing and editing code in various programming languages.
    VS Code is available for Windows, macOS, and Linux and is actively maintained by a team of developers at Microsoft.
- GitHub
  - Source code is hosted on GitHub and deployed using Heroku.
- Git
  - Used for version control
- Screen Recorder
  - Capture game play for title gif
  - https://chrome.google.com/webstore/detail/screen-recorder/hniebljpgcogalllopnjokppmgbhaden
- ezgif
  - Used to create the title gif (https://ezgif.com/)

**Python Packages**

- Colorama
  - Adding colored terminal text to the game (https://pypi.org/project/colorama/)
- Random
  - Used to pick random cards from the deck
- OS
  - Used to clear terminal after option selection, each completed hand and end of the game.
- String
  - the string module for working with string constants
- Pandas
  - the pandas library for data manipulation
- gspread
  - the gspread library for Google Sheets integration

## Testing

### Validator Testing

- CI Python Linter ([PEP CI Validator](https://pep8ci.herokuapp.com/))

  ![PEP CI Validator result](assets/images/cipythonlinter.png)

### Testing User Stories

|             Expectation (As a user, I want to...)             |                             Result (As a user, I...)                              |
| :-----------------------------------------------------------: | :-------------------------------------------------------------------------------: |
| Get a quick and thorough overview of the accounts & password  |         Can find my way around the app easily and quickly I one overview          |
| Every step in app there is a clear discription what to expect |        Can read the instructions from the options menu in a logical manner        |
|      Be able to enter the app simple click interactions       | Run the app by simply clicking the `y` or `n` to continue or complete the program |
|                  Receive correction messages                  |             When I inputed wrong the program tells me what to do next             |

### Fixed bugs

- Text line length greater 79 characters
- Clear Terminal positioning
- Whitespaces

## Deployment

### Version Control

The site was created using the Visual Code code editor and pushed to github to the remote repository [here](https://github.com/Harmonica-Men/Password-Manager) .

The following git commands were used throughout development to push code to the remote repo:

`git add .` - This command was used to add the file(s) to the staging area before they are committed.

`git commit -m “commit message”` - This command was used to commit changes to the local repository queue ready for the final step.

`git push` - This command was used to push all committed code to the remote repository on github.

### Deployment Through Heroku

The below steps were followed to deploy this project to Heroku:

- Go to Heroku and click "New" to create a new app.
- Choose an app name and region, click "Create app".
- Go to "Settings" and navigate to Config Vars. Add the following config variables:
  - PORT : 8000
- Navigate to Buildpacks and add buildpacks for Python and NodeJS (in that order).
- Navigate to "Deploy".
- Set the deployment method to Github and enter repository name and connect.
- Scroll down to Manual Deploy, select "main" branch and click "Deploy Branch".
- The app will now be deployed to heroku

The live link can be found [here](https://terminal-password-manager-2fad20bf8063.herokuapp.com/)

### Clone The Repository Code Locally

Navigate to the GitHub Repository you want to clone to use locally:

- Click on the code drop down button
- Click on HTTPS
- Copy the repository link to the clipboard
- Open your IDE of choice (git must be installed for the next steps)
- Type git clone copied-git-url into the IDE terminal

The project will now of been cloned on your local machine for use.

## Credits

### w3 schools

> Used to reference Python Structure

### Stack Overflow

> Used to reference different synthax issues from existing older boards. Also used to query clear function issues when I ran into them as referenced in the bug section.

## Acknowledgements

### Daisy McGirr

- My Mentor with Code Institute who has provided me with excellent feedback and guidance through this project.

[def]: #step-2-run-the-program
