import random
import gspread
from google.oauth2.service_account import Credentials
from words import words
import pyfiglet
from getkey import getkey, keys
from tabulate import tabulate
import time
import string


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
    print("Press h for highscore\n")
    key = getkey()
    while True:
        if key == keys.H:
            highscore_top_5()
            break

        elif key == keys.S:
            user_input()
            break

        else:
            user_input()
            break

def highscore_top_5():
    """
    Show top 5 highscore, lower attempts higher up on the list.
    Styled table from https://www.statology.org/create-table-in-python/
    Picking up data from google sheet, define header names and display table
    """
    highscore_list = SHEET.get_values("A2:6")
    col_names = ["Name", "Number of attempts"]

    print(tabulate(highscore_list, headers=col_names, tablefmt="fancy_grid"))


def user_input():
    """
    User write their game name and the game only accepts alphabets.
    If it's not only alphabets, re-enter their name
    """
    name = input("Write your name and press ENTER to start:\n").capitalize()
    if name.isalpha() is True:
        print(f"Hey, {name}!")
        time.sleep(1)
        print("Tip: There are some games that use compound words")
        time.sleep(1)
        print("Lets go!")
        time.sleep(1)
        print("Loading...")
        time.sleep(4)
        game_run()

    else: 
        print("Please enter your name using letter only")

def get_word(words):
    """
    Choosing random words from words.py and return with uppercase
    """
    word = random.choice(words)

    return word.upper()


def game_run():
    """
    Starts the game, the computer takes a random word. 
    Input is locked to letters only. 
    The player gets a predetermined number of tries (lives). 
    The letters guessed are printed. 
    If you guess wrong, you lose an attempt (life) If you guess 
    correctly or the life runs out, you are sent on to highscore_top_5.
    """
    word = get_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()

    lives = 6

    while len(word_letters) > 0 and lives > 0:

        print("You have", lives, "lives left and you have used these letters: ", " ".join(used_letters))

        word_list = [letter if letter in used_letters else '-' for letter in word]
        print("Current word: ", " ".join(word_list))

        user_letter = input("Guess a letter: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)

            else:
                lives = lives - 1
                print("Letter is not in the word.")

        elif user_letter in used_letters:
            print("You have already used that character. Please try again")

        else:
            print("Invalid character. Please try again")

    if lives == 0:
        print("You died, the word was:\n", word)
        time.sleep(2)
        highscore_top_5()
    else:
        print("congratulations, you guessed the correct word\n", word)
        time.sleep(2)
        highscore_top_5()


def play_again():
    """
    Function ask user if they want to play again.
    """
    response = input("Would you like to play again? Enter 'Y' for Yes or 'N' for No.\n").lower()
    if response == "y":
        game_run()
    else:
        print("Hope you had fun playing the game. See you next time =)")


def start_game():
    start_menu()
    user_input()
    play_again()
    word_letters()
    game_run()


start_game()

