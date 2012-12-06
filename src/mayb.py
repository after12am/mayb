import os, sys

def main():
    
    if len(sys.argv) <= 1: return
    
    if sys.argv[1] == 'setup':
        from core.db import setup
        setup()
    if sys.argv[1] == 'crawle':
        from core.pinterest import crawle
        crawle()
    if sys.argv[1] == 'train':
        from core.recommend import cluster
        cluster()

if __name__ == '__main__': main()