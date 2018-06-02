#!/usr/bin/env python3

from argparse import ArgumentParser
from PIL import Image
from PIL.ImageOps import invert
import numpy as np


def generate(args):
    """ generate puzzle """
    
    def img_to_spr(img):
        """ split image into 10x10 sprites """
        
        return [img.crop((x, y, x+10, y+10)) for y in range(0, img.size[1], 10) for x in range(0, img.size[0], 10)]
    
    
    def color_spr(spr, color):
        """ replace black in sprite with another color """
        
        color = np.array(color)
        x, y, z = *spr.size, 3  # sprite dimensions
        spr = np.array(spr).reshape((x*y, z))  # reshape
        spr = np.hstack([color if sum(p) == 0 else p for p in spr]).reshape((x, y, z)).astype(np.uint8)  # color
        return Image.fromarray(spr)
    
    
    # ascii characters corresponding to `tileset.png`
    ascii_chr = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    # map A-Z -> 1-26
    chr_num = dict(zip(ascii_chr[33:59], range(1, 27)))
    chr_num[' '] = 27
    
    # black letters on white background (by inverting the colours)
    img = invert(Image.open('tileset.png').convert('1').convert('RGB'))
    ascii_spr = img_to_spr(img)[32:127]
    spr = dict(zip(ascii_chr, ascii_spr))
    
    # append padding so width % 3 == 0
    if len(args.code) % 3:
        code = args.code + ' ' * (3-len(args.code)%3)
    else:
        code = args.code
    
    # insert the clue
    puz = Image.new('RGB', (10*3, 10*(len(code)//3+1)))
    puz.paste(color_spr(spr['R'], (255, 0, 0)), (0, 0))  # R
    puz.paste(color_spr(spr['G'], (0, 255, 0)), (10, 0))  # G
    puz.paste(color_spr(spr['B'], (0, 0, 255)), (20, 0))  # B
    
    # create the puzzle
    for i, char in enumerate(code):
        x, y = i%3, i//3+1  # determine the letter position
        color = np.random.randint(256, size=3)  # randomise the RGB values
        color[x] = chr_num[char]  # set the channel to the alphabet number
        puz.paste(color_spr(spr['RGB'[x]], color), (10*x, 10*y))  # insert the code
        
    puz.save(args.fname)
    print("Clue: proper channels")
    print("Puzzle saved:", args.fname)
    
    
def solve(args):
    """ solve puzzle """
    
    # map 1-26 -> A-Z
    num_chr = dict(zip(range(1, 28), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '))
    
    puz = Image.open(args.fname)
    
    code = ''
    for y in range(10, puz.size[1], 10):  # start from the second row
        for x in range(0, puz.size[0], 10):
            for _, color in puz.crop((x, y, x+10, y+10)).getcolors():
                if sum(color) != 765:  # not white (255, 255, 255)
                    code += num_chr[color[x//10]]  # use value from the RGB channel
                    break
    print("Code:", code)
    
    
if __name__ == '__main__':
    description = """ This puzzle hides the code in the RGB channels. """
    parser = ArgumentParser(description=description)
    parser.add_argument('--code', default='STATIC', type=str, help='message to hide')
    parser.add_argument('--fname', default='puzzle.png', help='.png file')
    args = parser.parse_args()
    generate(args)
    solve(args)
    
