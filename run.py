import random
import gspread
from google.oauth2.service_account import Credentials
from words import words
import pyfiglet
from getkey import getkey, keys

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hangman_highscore')


highscore = SHEET.worksheet('highscore')

data = highscore.get_all_values()

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
    print(
        "Greetings and welcome to Gaming Hangman!\n",
        "Various titles of PC games will be randomly selected,\n",
        "and you have to guess them correctly before your lives run out.\n",
        "In order to survive, you have five attempts.\n",
        "Wishing you the best!\n"
    )
    print("Press s for start")
    print("Press h for highscore")
    key = getKey()
    while True:
        if key == keys.s:
            startgame()
        elif key == keys.h:
            highscore()
        else:
            startgame()

def startgame():
    start_menu()

startgame()

