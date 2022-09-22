import random
import gspread
from google.oauth2.service_account import Credentials
from words import words
import pyfiglet
from getkey import getkey, keys
from tabulate import tabulate
import time


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hangman_highscore').worksheet('highscore')


def start_menu():
    """
    Start menu with figlet welcome script from
    https://www.devdungeon.com/content/create-ascii-art-text-banners-python
    Greetings with instructions and choose if user want to start or
    see highscore.
    """
    welcome_message = pyfiglet.figlet_format("Welcome")
    print(welcome_message)
    print("")
    time.sleep(2)
    print(
        "Greetings and welcome to Gaming Hangman!\n",
        "Various titles of PC games will be randomly selected,\n",
        "and you have to guess them correctly before your lives run out.\n",
        "In order to survive, you have five attempts.\n",
        "Wishing you the best!\n"
    )
    time.sleep(4)
    print("Press s for start")
    print("Press h for highscore")
    key = getkey()
    while True:
        if key == keys.H:
            highscore_top_5()
            break

        elif key == keys.S:
            start_game()
            break

        else:
            start_game()


def highscore_top_5():
    """
    Show top 5 highscore, lower attempts higher up on the list.
    Styled table from https://www.statology.org/create-table-in-python/
    """
    #create data
    highscore_list = SHEET.get_values("A2:6")
    #define header names
    col_names = ["Name", "Number of attempts"]
    #display table
    print(tabulate(highscore_list, headers=col_names, tablefmt="fancy_grid"))


def start_game():
    start_menu()
    

start_game()