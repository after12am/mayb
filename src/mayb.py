import os, sys
from core.db import setup
from core.pinterest import crawle
from core.recommend import cluster, train

commands = ['setup', 'crawle', 'train']

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in commands:
            try:
                eval(sys.argv[1] + '()')
            except:
                print 'failed to execute %s()' % sys.argv[1]
    else:
        pass

if __name__ == '__main__': main()