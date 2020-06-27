import os
import re
import sys
import requests

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
# joke = 'What does an angry pepper do?'
# punchline = 'It gets jalopeno face.'


def get_joke():
    joke_requests_remaining = 3
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
    joke_requests_remaining -= 1
    get_joke()
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
            print(f'\nNice Job! Laugh Away!!\n')
            break
        print(gameboard)
        print(f'\nNumber of guesses remaining...{num_of_chances_remaining}\n')
        print(body_dict[num_of_chances_remaining])
        print(f"\nIncorrect guesses: {' '.join(wrong_letters)}")
        guess = input("Guess a letter: ").lower()
        if guess not in punchline.lower():
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
