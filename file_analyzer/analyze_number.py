import sys
import os
import subprocess
import json


def read_file_signature(file_name, num_bytes=8):
    with open(file_name, "rb") as f:
        magic = f.read(num_bytes)

    return magic.hex()


def get_file_extension(file_name):
    root, ext = os.path.splitext(file_name)
    return ext


def file_extension_comparison(file_extension):
    with open("signatures.json", "r") as signatures:
        data = json.load(signatures)
    
    potential_signatures = []
    for signatures in data:
        if file_extension == signatures['suffix']:
            potential_signatures.append(signatures['sign'])
    
    return potential_signatures


def main():

    
    print("******************************")
    print("Enter file path to analyze: ")
    file = input()

    if os.path.isfile(file):
        # get file extension
        file_ext = get_file_extension(file)
        
        if file_ext:
            print(f"File Extension: {file_ext}")
        
        file_sig = read_file_signature(file)
        print(f"Raw Hex File Signature: {file_sig}")
        print('\n' * 5)

        # Run the file command

        print("Output of `file` command: ")
        subprocess.run(["file", file])

        print('\n' * 5)

        # compare the file extension and magic number against a database

        potential_signatures = file_extension_comparison(file_sig, file_ext)

        print(f"Signatures for the {file_ext} file extension: ")
        for sig in potential_signatures:
            print(sig)


        print('\n' * 2)
        print("******************************")
        sys.exit()

if __name__=="__main__":
    main()