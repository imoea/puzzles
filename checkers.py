#!/usr/bin/env python3

from argparse import ArgumentParser
from PIL import Image
import random


def generate(args):
    """ generate puzzle """
    
    def img_to_spr(img):
        """ split image into 10x10 sprites """

        height, width = img.size
        return [img.crop((x, y, x+10, y+10)) for y in range(0, height, 10) for x in range(0, width, 10)]
    
    
    # string->braille map
    with open('braille.txt') as f:
        tokens = [line.split() for line in f.read().strip().split('\n')]

    braille = dict(tokens)
    for i in range(len(tokens)):
        tokens[i][1] = len(tokens[i][0])

    start, end = [], []
    code = args.code

    # convert code to braille
    for t in tokens[:44]:
        if code[:t[1]] == t[0]:
            start.append(t[0])
            code = code[t[1]:]
            break

    for t in tokens[-2:]:
        if code[-t[1]:] == t[0]:
            end.append(t[0])
            code = code[:-t[1]]
            break

    # reorder the tokens
    tokens = tokens[:18] + tokens[44:50] + tokens[18:44]

    # continue converting the code to braille
    while code:
        for t in tokens:
            if code[:t[1]] == t[0]:
                start.append(t[0])
                code = code[t[1]:]
                break

    tokens = start + end

    # braille can be stored as 3 binary strings
    # this is primarily used for solving due to its ease of reading
    puz = [''] * 3
    for t in tokens:
        for i in range(3):
            puz[i] += braille[t][i*2:i*2+2]
            
    # load the tileset and use only the black and white circles
    img = Image.open('tileset.png').convert('1')  # white on black
    spr = img_to_spr(img)
    black, white = spr[0], spr[219]
    map_ = {'0': {True: spr[7], False: spr[10]}, '1': {True: spr[9], False: spr[8]}}
    
    size = len(puz[0]) * 10  # length of the board
    png = Image.new('L', (size, size))
    # draw the checkers board
    for i in range(0, size, 10):
        for j in range(0, size, 10):
            if i%20 == 0:
                png.paste(white if j%20 == 0 else black, (j, i))
            else:
                png.paste(black if j%20 == 0 else white, (j, i))

    # populate the board with checkers piece according to the braille
    for e, i in enumerate(range(size//2-20, size//2+10, 10)):
        for f, j in enumerate(range(0, size, 10)):
            if i%20 == 0:
                png.paste(map_[puz[e][f]][j%20 != 0], (j, i))
            else:
                png.paste(map_[puz[e][f]][j%20 == 0], (j, i))
                
    png.save(args.pngname)
    print("Clue: touch the pieces")
    print("Puzzle saved:", args.pngname, "(PNG)")
    
    puz = '\n'.join(puz)
    
    with open(args.txtname, 'w') as f:
        f.write(puz)
    print("Puzzle saved:", args.txtname, "(TXT)")
    
    
def solve(args):
    """ solve puzzle """
    
    with open('braille.txt') as f:
        braille = [line.split() for line in f.read().strip().split('\n')]

    braille = {y: x for x, y in braille}
    
    with open(args.txtname) as f:
        puz = f.read().split()
        
    # read braille from the 3 binary strings
    code = ''
    while puz[0]:
        key = ''
        for i in range(3):
            key += puz[i][:2]
            puz[i] = puz[i][2:]
        code += braille[key]
    
    print("Code:", code)
    
    
if __name__ == '__main__':
    description = """ This puzzle hides the message as braille on an NxN checkers board.
    It is recommended for the braillie equivalent to be exactly 8 dots wide so as to
    maintain the illusion of a standard checkers board. """
    parser = ArgumentParser(description=description)
    parser.add_argument('--code', default='FEEL', type=str, help='message to hide')
    parser.add_argument('--pngname', default='puzzle.png', help='.png file')
    parser.add_argument('--txtname', default='puzzle.txt', help='.txt file')
    args = parser.parse_args()
    generate(args)
    solve(args)
    
