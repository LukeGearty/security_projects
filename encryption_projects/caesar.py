#!/usr/bin/python3
import sys

def caesar_cipher(text, offset):
    result = ""

    for char in text:
        if char.isupper():
            result += chr((ord(char) + offset - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + offset - 97) % 26 + 97)
        else:
            result += char
        
    return result


def main():
    offset = int(sys.argv[1])
    text = input("Enter the text you wish to encrypt: ")

    print(caesar_cipher(text, offset))    

if __name__=="__main__":
    main()