import sys
import argparse
import binascii
import base64
import urllib


class Extender(argparse.Action):

    def __call__(self,parser,namespace,values,option_strings=None):

        # Need None here incase `argparse.SUPPRESS` was supplied for `dest`
        dest = getattr(namespace,self.dest,None)

        # print dest,self.default,values,option_strings
        if(not hasattr(dest,'extend') or dest == self.default):
            dest = []
            setattr(namespace,self.dest,dest)
            # if default isn't set to None, this method might be called
            # with the default as `values` for other arguements which
            # share this destination.
            parser.set_defaults(**{self.dest:None})

        try:
            dest.extend(values)
        except ValueError:
            dest.append(values)

        #another option:
        #if not isinstance(values,basestring):
        #    dest.extend(values)
        #else:
        #    dest.append(values) #It's a string.  Oops.

def ascii2bin(x):
    return bin(int(binascii.hexlify(x), 16))

def bin2ascii(x):
    n = int('0b'+x, 2)
    print binascii.unhexlify('%x' % n)
    return binascii.unhexlify('%x' % n)

def str2base64(x):
    return base64.b64encode(x)

def base642str(x):
    return base64.b64decode(x)

def str2hex(x):
    hex_int = int(x, 16)
    new_int = hex_int + 0x200
    return hex(new_int)
    #return hex(new_int)[2:]       # If you don't like the 0x in the beginning

def str2url(x):
    return urllib.quote_plus(x)

#####################################################################################################
def new_parser(args):

    parser = argparse.ArgumentParser()
    parser.add_argument('--ascii2bin',              nargs='*',      dest='ascii2bin',           action=Extender)
    parser.add_argument('--bin2ascii',              nargs='*',      dest='bin2ascii',           action=Extender)
    parser.add_argument('--str2base64',             nargs='*',      dest='str2base64',          action=Extender)
    parser.add_argument('--base642str',             nargs='*',      dest='base642str',          action=Extender)
    parser.add_argument('--str2hex',                nargs='*',      dest='str2hex',             action=Extender)
    parser.add_argument('--str2url',                nargs='*',      dest='str2url',             action=Extender)


    return parser.parse_args()


##############################################################################################

def run():

    if len(sys.argv) <=1:
        return

    args = new_parser(sys.argv[1:])

    if(args.ascii2bin):
        data = ascii2bin(args.ascii2bin[0])
    if(args.bin2ascii):
        data = bin2ascii(args.bin2ascii[0])
    if(args.str2base64):
        data = str2base64(args.str2base64[0])
    if(args.base642str):
        data = base642str(args.base642str[0])
    if(args.str2hex):
        data = str2hex(args.str2hex[0])
    if(args.str2url):
        data = str2url(args.str2url[0])

    return data


##############################################################################################

if __name__ == "__main__":

    data = run()
    sys.stdout.write(data)
    #exit the program
    sys.exit()
