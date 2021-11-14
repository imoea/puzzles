#!/usr/bin/env python3

from argparse import ArgumentParser
from random import choice, randint


# load required vocabulary
with open('adjectives.txt') as f:
    adj = f.read().split()
    
with open('nouns.txt') as f:
    nn = f.read().split()

with open('morse.txt') as f:
    morse = dict(x.split() for x in f.read().split('\n'))
        
        
def generate(args):
    """ generate puzzle """
    
    def random_username(sep=''):
        """ generate a random username """

        # hide the code in the separator
        username = choice(adj).capitalize() + sep + choice(nn).capitalize()
        if randint(0, 1):  # append random numbers to mislead
            for _ in range(randint(2, 4)):
                username += str(randint(0, 9))
        return username
    
        
    # create the puzzle
    puz = []
    for i, char in enumerate(args.code):
        for signal in morse[char]:
            # hide the signal in a random username
            puz.append(random_username(signal))
        if i+1 < len(args.code):
            puz.append(random_username())  # add a pause
    puz = '\n'.join(puz)
            
    with open(args.fname, 'w') as f:
        f.write(puz)
    print("Clue: connect the dots")
    print("Puzzle saved:", args.fname)
    
    
def solve(args):
    """ solve puzzle """
    
    chars = {v: k for k, v in morse.items()}
    
    with open(args.fname) as f:
        puz = f.read().split()
    
    # extract the morse code
    code = char = ''
    while puz:
        username = puz.pop(0)
        if '.' in username:
            char += '.'
        elif '_' in username:
            char += '_'
        else:
            code += chars[char]
            char = ''
    code += chars[char]
    
    print("Code:", code)
    
    
if __name__ == '__main__':
    description = """ This puzzle hides morse code in the dots and dashes
    commonly found in usernames. """
    parser = ArgumentParser(description=description)
    parser.add_argument('--code', default='TELEGRAPH', type=str, help='message to hide')
    parser.add_argument('--fname', default='puzzle.txt', help='.txt file')
    args = parser.parse_args()
    generate(args)
    solve(args)
    
