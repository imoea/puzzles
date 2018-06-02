#!/usr/bin/env python3

from argparse import ArgumentParser
from PIL import Image
from PIL.ImageOps import invert
import numpy as np
import random
import scipy.misc as sm


def generate(args):
    """ generate puzzle """
    
    def img_to_spr(img):
        """ split image into 10x10 sprites """
        
        height, width = img.size
        return [img.crop((x, y, x+10, y+10)) for y in range(0, height, 10) for x in range(0, width, 10)]


    def code_to_code(code):
        """ scramble the code """

        if len(code) % 2:
            code += '$'  # append padding
        _code = ''.join(code[i] + code[i+len(code)//2] for i in range(len(code)//2))
        if _code[-1] == '$':
            _code = _code[:-1]  # remove padding
        return _code
    
    
    # ascii characters corresponding to `tileset.png`
    ascii_chr = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

    # white letters on black background
    img = Image.open('tileset.png').convert('1')
    ascii_spr = img_to_spr(img)[32:127]
    spr = dict(zip(ascii_chr, ascii_spr))

    # black letters on white background (by inverting the colours)
    img_inv = invert(img.convert('RGB')).convert('1')
    ascii_spr_inv = img_to_spr(img_inv)[32:127]
    spr_inv = dict(zip(ascii_chr, ascii_spr_inv))
    
    code = code_to_code(args.code.upper())  # initial scramble
    size = len(code)  # puzzle size is dependent on code length
    pos = [(random.randint(0, size-1), i) for i in range(size)]  # randomise code positions

    # print the puzzle
    puz = Image.new('L', (10*size, 10*size))
    for j, (x, y) in enumerate(pos):
        char = code[j]
        
        if j % 2 == 0:  # BLACK
            # increase whiteness by 1
            values = 255*np.array(spr_inv[char], 'uint8') + 1*np.array(spr[char], 'uint8')
            puz.paste(Image.fromarray(values, mode='L'), (10*x, 10*y))
            # randomise the other letters in the row
            for i in range(size):
                if i != x:
                    puz.paste(random.choice(ascii_spr_inv[33:59]), (10*i, 10*y))
                    
        else:  # WHITE
            # decrease whiteness by 1
            values = 255*np.array(spr_inv[char], 'uint8') + 254*np.array(spr[char], 'uint8')
            puz.paste(Image.fromarray(values, mode='L'), (10*x, 10*y))
            # fill the rest of the row with spaces
            for i in range(size):
                if i != x:
                    puz.paste(ascii_spr_inv[0], (10*i, 10*y))

    puz.save(args.fname)
    print("Clue: black nor white")
    print("Puzzle saved:", args.fname)
    
    
def solve(args):
    """ solve puzzle """
    
    puz = sm.imread(args.fname, mode='L')
    arr = [0 if p == 255 else p for p in puz.flatten()]  # remove white
    arr = [127 if p == 0 else p for p in arr]  # remove black
    sm.imsave('code.png', np.reshape(arr, puz.shape))
    print("Code saved: code.png")
    
    
if __name__ == '__main__':
    description = """ This puzzle exploits the fact that it's almost impossible
    for a human being to differentiate between minute changes in color intensity. """
    parser = ArgumentParser(description=description)
    parser.add_argument('--code', default='TECHNICOLOR', type=str, help='message to hide')
    parser.add_argument('--fname', default='puzzle.png', help='.png file')
    args = parser.parse_args()
    generate(args)
    solve(args)
    
