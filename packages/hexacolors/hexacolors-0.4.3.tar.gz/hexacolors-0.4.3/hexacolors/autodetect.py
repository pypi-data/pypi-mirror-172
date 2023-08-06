import string

from .api import hexadecimal, hsl, rgb, cmyk
from .str import stringcolor

def autodetect(args:str) -> str:

    if args[0] == '#':

        hexadecimal(args)

    elif args.count('%') == 2:

        hsl(args)

    elif args.count(',') == 2:

        rgb(args)
    
    elif args.count(',') == 3:

        cmyk(args)

    elif args[0] in list(string.digits):

        hexadecimal(args)
    
    elif args[0] in list(string.ascii_letters):

        try:

            stringcolor(args)

        except:

            hexadecimal(args)

    else:

        print('ERROR: Not indentify the type')
