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


# comparing based on strings
def signature_match(file_sig, comparison_sig):
    file_sig = file_sig.lower()
    comparison_sig = comparison_sig.lower()
    return file_sig.startswith(comparison_sig)


# more robust checking based on prefixes

def signature_match_prefixes(file_sig, comparison_sig):
    prefix = []
    for c1, c2 in zip(file_sig, comparison_sig):
        if c1 == c2:
            prefix.append(c1)
        else:
            break
    return "".join(prefix) if prefix else None

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
        file_command = subprocess.run(["file", file])
        print(file_command)

        print('\n' * 5)

        # compare the file extension and magic number against a database

        potential_signatures = file_extension_comparison(file_ext)
        is_discrepancy = True

        print(f"Signatures for the {file_ext} file extension: ")
        for sig in potential_signatures:
            if file_sig.lower() in sig.lower() or sig.lower() in file_sig.lower():
                is_discrepancy = False
            elif signature_match(file_sig, sig) or signature_match(sig, file_sig):
                is_discrepancy = False
            elif signature_match_prefixes(file_sig, sig):
                is_discrepancy = False
            print(sig)
        

        # compare the file_ext against the signatures
        print('\n')
        if is_discrepancy:
            print("[!] Potential Discrepancy Found")
            print(f"File's Signature: {file_sig}")

            print(f"[!] This file signature was not found in the potential signatures for a {file_ext} file")
            print("[!] Investigation Further Recommended")

        else:
            print(f"No discrepancy found, {file} and its signatures and extensions match")
            print("If you are unsure, further investigation may be needed")
        print('\n' * 2)

        # create JSON output

        json_output = {
            "path": file,
            "extension": file_ext,
            "File Signature": file_sig,
            "File Command": file_command,
            "Match": not is_discrepancy,
        }

        print(json_output)

        print('\n')
        print("******************************")
        sys.exit()


if __name__=="__main__":
    main()