import random
import gspread
from google.oauth2.service_account import Credentials
from words import words
import pyfiglet
from getkey import getkey, keys
from tabulate import tabulate
import time
import string
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hangman_highscore').worksheet('highscore')

# global variables
ATTEMPTS = 0
USER_NAME = ""
LIVES = 6


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
    print("Greetings and welcome to Gaming Hangman!\n\n",
          "Various titles of PC games will be randomly selected,\n",
          "and you have to guess them correctly before your "
          "lives run out.\n\n",
          "In order to survive, you have six attempts.\n\n",
          "You got plus ten extra attempts if you die...\n\n",
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
            break
        else:
            print("Loading...")
            time.sleep(1)
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
    User write their game name.
    Is username is empty, error code and try again.
    """
    global USER_NAME
    USER_NAME = input(
        "Write your name and press ENTER to start:\n").capitalize()
    if len(USER_NAME) == 0:
        while len(USER_NAME) == 0:
            print("Error...")
            USER_NAME = input(
                "Please write your name and press ENTER:\n").capitalize()
    print(f"Hey, {USER_NAME}!")
    time.sleep(1)
    print("Tip: There are some games that use compound words")
    time.sleep(1)
    print("Lets go!")
    time.sleep(1)
    print("Loading...")
    time.sleep(4)
    return USER_NAME


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
    The player gets a predetermined number of tries (lives) and
    attempts.
    The letters guessed are printed + attempts and lives calculates
    If you guess wrong, you lose an life and +1 on attempts.
    If you die, +10 attempts
    """
    global ATTEMPTS
    global LIVES
    word = get_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()

    while len(word_letters) > 0 and LIVES > 0:

        print("Attempts:", ATTEMPTS, "\n")
        print("You have", LIVES,
              "lives left and you have used these letters: ",
              " ".join(used_letters))
        word_list = [
            letter if letter in used_letters else '-' for letter in word]
        print("Current word: ", " ".join(word_list))

        user_letter = input("Guess a letter: \n").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)

            else:
                LIVES = LIVES - 1
                ATTEMPTS = ATTEMPTS + 1
                print("Letter is not in the word.\n")

        elif user_letter in used_letters:
            print("You have already used that character. Please try again\n")

        else:
            print("Invalid character. Please try again\n")

    if LIVES == 0:
        ATTEMPTS = ATTEMPTS + 10
        print("You died, the word was:\n", word)

    else:
        print("congratulations, you guessed the correct word\n", word)


def score_update():
    """
    Update and add Username and attempts to google sheets
    Printing user attempts and 5 sec delays for
    google sheet to update so a new highscore will show up
    """
    global USER_NAME
    global ATTEMPTS
    SHEET.insert_row([USER_NAME, ATTEMPTS], index=2)
    print("Highscore loading...")
    print("Your attempts: ", ATTEMPTS)
    time.sleep(5)
    highscore_top_5()


def reset_attempts_lives():
    """
    Resets lives and attempts
    """
    global ATTEMPTS
    global LIVES
    LIVES = 6
    ATTEMPTS = 0


def play_again():
    """
    Ask user if they want to play again.
    Resets attempts and lives
    """
    reset_attempts_lives()
    response = input(
        "Would you like to play again? Enter 'Y' for Yes"
        " or 'N' for No.\n").lower()
    if response == "y":
        main()
    else:
        print("Hope you had fun playing the game. See you next time =)")
        sys.exit(0)


def start_game():
    """
    Run program functions
    """
    start_menu()
    user_input()
    main()


def main():
    """
    Run game functions
    """
    get_word(words)
    game_run()
    score_update()
    play_again()


start_game()
