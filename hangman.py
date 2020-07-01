import os
import re
import sys
import requests


# game settings
body_dict = {}
body_dict[6] = ('--|')
body_dict[5] = (f'{body_dict[6]}\n  O')
body_dict[4] = (f'{body_dict[5]}\n /')
body_dict[3] = (f'{body_dict[4]}|')
body_dict[2] = (f'{body_dict[3]}\\')
body_dict[1] = (f'{body_dict[2]}\n /')
body_dict[0] = (f'{body_dict[1]} \\')
guessed_letters = []
wrong_letters = []
joke_requests_remaining = 4
INITIAL_GUESSES = 6
num_of_chances_remaining = INITIAL_GUESSES
score = 0
# joke = 'What does an angry pepper do?'
# punchline = 'It gets jalopeno face.'

# in-game messages
thanks = "Thanks for playing!"
start = "Start a new game(y or n)?: "
keep_going = "Do you want to continue (y or n)?: "
winner = '\nNice Job! Laugh Away!!\n'
new_score = '\nYour currant score: '
chances = '\nNumber of guesses remaining...'
wrong = "\nIncorrect guesses: "
lose = '\nClose but no cigar\n'


def get_joke():
    headers = {'accept': 'application/json'}
    for _ in range(joke_requests_remaining):
        response = requests.get('https://icanhazdadjoke.com/', headers=headers)
        data = response.json()
        text = data['joke']
    # restrict joke format from API response to two part joke
        joke_match = re.search(r'(.+[.?!])(.+[.?!])', text)
        if joke_match:
            joke = joke_match.group(1).strip()
            punchline = joke_match.group(2).strip()
            return joke, punchline
    # discard joke if there is no distinct punchline
        print('Did not get a good joke from API.')
    sys.exit(1)


def update_blanks(punchline):
    """display the gameboard"""
    display = []
    for char in punchline.lower():
        if not char.isalpha() or char in guessed_letters:
            display.append(char)
        else:
            display.append('_')
    display[0] = display[0].upper()
    return ' '.join(display)


def continue_game(msg):
    """continue or reset game"""
    choice = input(msg)
    if choice not in ('y', 'n'):
        continue_game(msg)
    return True if choice == 'y' else False


def init(lost=False):
    """Initialize all game settings"""
    global num_of_chances_remaining, score
    num_of_chances_remaining = INITIAL_GUESSES
    guessed_letters.clear()
    wrong_letters.clear()
    if lost:
        score = 0


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    global num_of_chances_remaining, score
    init()
    joke, punchline = get_joke()

    while True:
        clear_screen()
        print(f'{new_score}{score}')
        print(f'\n{joke}\n')
        gameboard = update_blanks(punchline)
        if '_' not in gameboard:
            score += (100 // INITIAL_GUESSES) * num_of_chances_remaining
            print(f'{punchline}\n{winner}\n{new_score}{score}\n')
            if continue_game(keep_going):
                init()
                joke, punchline = get_joke()
                continue
            else:
                print(thanks)
                break
        print(f'{gameboard}\n')
        print(f"{chances}{num_of_chances_remaining}\n{wrong}{' '.join(wrong_letters)}\n")
        print(f'{body_dict[num_of_chances_remaining]}\n')
        guess = input("Guess a letter: ").lower()
        if guess not in punchline.lower():
            wrong_letters.append(guess)
            if guess not in guessed_letters:
                num_of_chances_remaining -= 1
        if guess not in guessed_letters:
            guessed_letters.append(guess)
        if not num_of_chances_remaining:
            clear_screen()
            print(f'{body_dict[num_of_chances_remaining]}\n{lose}')
            if continue_game(start):
                init(lost=True)
                joke, punchline = get_joke()
            else:
                print(thanks)
                break


if __name__ == '__main__':
    main()
