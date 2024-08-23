#!/usr/bin/python3
import sys


def transpose(text, key):
    grid = [''] * key
    
    for col in range(key):
        current = col

        while current < len(text):
            grid[col] += text[current]
            current += key
    
    return ''.join(grid)

def main():
    key = int(sys.argv[1])
    text = input("Enter your message: ")
    print(transpose(text, key))

    
if __name__=="__main__":
    main()