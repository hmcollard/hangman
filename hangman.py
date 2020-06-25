import os
import re
import sys
import requests

"""
A Hangman-style Dad Joke game!

TODO:
- setup:
    - [DONE]obtain a random phrases - dad jokes API (https://icanhazdadjoke.com/)
    - [DONE]initialize number of chances(6)
    - [DONE]split joke and punch line
    - [DONE]represent the phrase as a series of underscores
    - display the outcome (the person figure)
    - [DONE]maintain a list of guessed letters
- game loop:
    [DONE]- prompt user to enter a letter
    - [DONE]determine whether the users guess is in the phrase
    - [DONE]provide feedback about the users guess
        - [DONE]if correct, display letter where it belongs in the phrase
        - [DONE]if incorrect, display the next body part
    - [DONE]win: fill the phrase
    - [DONE]lose: chances = 0
-[DONE] display all guessed letters
- [DONE]case insensitive bug
TODO: figure out how to make it a two person competing game
"""
body_dict = {}
body_dict[6] = (f'--|')
body_dict[5] = (f'{body_dict[6]}\n  O')
body_dict[4] = (f'{body_dict[5]}\n /')
body_dict[3] = (f'{body_dict[4]}|')
body_dict[2] = (f'{body_dict[3]}\\')
body_dict[1] = (f'{body_dict[2]}\n /')
body_dict[0] = (f'{body_dict[1]} \\')
guessed_letters = []
wrong_letters = []
joke_requests_remaining = 3
joke = 'What does an angry pepper do?'
punchline = 'It gets jalopeno face.'


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
    print(
        f'Did not get a good joke. {joke_requests_remaining} tries left.')
    sys.exit(1)


def update_blanks(punchline):
    display = []
    for char in punchline.lower():
        if not char.isalpha() or char in guessed_letters:
            display.append(char)
        else:
            display.append('_')
    display[0] = display[0].upper()
    return ' '.join(display)


def main():
    num_of_chances_remaining = 6
    joke = get_joke()
    text, punchline = joke

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'\n{text}\n')
        gameboard = update_blanks(punchline)
        if '_' not in gameboard:
            print(punchline)
            print(f'\nNice One! Laugh Away!!\n')
            break
        print(gameboard)
        print(f'\nNumber of guesses remaining...{num_of_chances_remaining}\n')
        print(body_dict[num_of_chances_remaining])
        print(f"\nPrevious guesses: {' '.join(wrong_letters)}")
        guess = input("Guess a letter: ").lower()
        if guess not in punchline:
            wrong_letters.append(guess)
            if guess not in guessed_letters:
                num_of_chances_remaining -= 1
        if guess not in guessed_letters:
            guessed_letters.append(guess)
        if not num_of_chances_remaining:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(body_dict[num_of_chances_remaining])
            print(f'\nClose but no cigar\n')
            break


if __name__ == '__main__':
    main()