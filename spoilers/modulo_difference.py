#!/usr/bin/env python3

from argparse import ArgumentParser
import random


def generate(args):
    """ generate puzzle """
    
    chars = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', range(1, 27)))
    
    # choose a random starting point
    clue = []
    puz = [random.randint(0, 25)]
    for i in range(len(args.code)):
        # randomly add or subtract the value of the letter from the previous point
        mod = random.choice([-1, 1])
        clue.append('+' if mod == 1 else '-')
        puz.append((puz[-1] + mod * chars[args.code[i]]) % 26)
    clue = ''.join(clue)
    puz = ', '.join(map(lambda x: str(x + 1), puz))  # string them up
    
    with open(args.fname, 'w') as f:
        f.write(puz)
    print("Clue:", clue)
    print("Puzzle saved:", args.fname)
    
    
def solve(args):
    """ solve puzzle """
    
    chars = dict(zip(range(1, 27), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    
    with open(args.fname) as f:
        puz = list(map(int, f.read().split(', ')))
        
    # collect the absolute difference of every consecutive pair of numbers

    # note that due to random addition/subtraction during generation,
    # each position might be one of two possible letters

    # it is hence better to decode by hand
    code = [abs(puz[i-1] - puz[i]) for i in range(1, len(puz))]
    code = ''.join(chars[i] for i in code)  # string them up
    
    print("Code:", code)
    
    
if __name__ == '__main__':
    description = """ This puzzle hides the message in the absolute difference
    between every consecutive pair of numbers. """
    parser = ArgumentParser(description=description)
    parser.add_argument('--code', default='CHANGE', type=str, help='message to hide')
    parser.add_argument('--fname', default='puzzle.txt', help='.txt file')
    args = parser.parse_args()
    generate(args)
    solve(args)
    
