#!/usr/bin/env python3

from argparse import ArgumentParser


def generate(args):
    """ generate puzzle """
    
    chars = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', range(26)))
    
    # map the first letter to its number 1-26
    puz = [chars[args.code[0]] + 1]
    for i in range(1, len(args.code)):
        # compute the difference needed to get to the next letter modulo 26
        puz.append((chars[args.code[i]] - chars[args.code[i-1]]) % 26)
    puz = ', '.join(map(str, puz))  # string them up
            
    with open(args.fname, 'w') as f:
        f.write(puz)
    print("Clue: keep going")
    print("Puzzle saved:", args.fname)
    
    
def solve(args):
    """ solve puzzle """
    
    chars = dict(zip(range(26), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    
    with open(args.fname) as f:
        puz = list(map(int, f.read().split(', ')))
        
    # get the first number modulo 26
    code = [puz[0] - 1]
    for i in range(1, len(puz)):
        # add each following number modulo 26 for the rest of the code
        code.append((puz[i] + code[-1]) % 26)
    code = ''.join(chars[i] for i in code)  # string them up
    
    print("Code:" , code)
    
    
if __name__ == '__main__':
    description = """ This puzzle hides the message
    using a sequence of modulo additions. """
    parser = ArgumentParser(description=description)
    parser.add_argument('--code', default='ELEMENTARY', type=str, help='message to hide')
    parser.add_argument('--fname', default='puzzle.txt', help='.txt file')
    args = parser.parse_args()
    generate(args)
    solve(args)
    
