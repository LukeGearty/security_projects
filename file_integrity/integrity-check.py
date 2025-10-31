import sys
import json 
import os 
import hashlib

BASE_DIR = "baselines"
BASE_FILE = "baselines.json"

def compute_hash(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)

    try:
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)
    except (PermissionError, FileNotFoundError) as e:
        print(f"Skipping {file_path}: {e}")
    return hash_func.hexdigest()



def valid_directory(directory):
    return os.path.isdir(directory)
    


def in_file(master_directory, directory):
    return master_directory.get(directory)



def compute_hash_directory(directory):    
    data = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            file_hash = compute_hash(full_path)
            relative_path = os.path.relpath(full_path, directory)
            data[relative_path] = file_hash
    return data


def append_to_file(directory, data: dict):
    wrapped_data = {directory: data}
    permissions = 0o700 #only root

    os.makedirs(BASE_DIR, mode=permissions, exist_ok=True)
    output_path = os.path.join(BASE_DIR, BASE_FILE)

    if os.path.exists(output_path):
        with open(output_path, "r") as json_file:
            try:
                all_data = json.load(json_file)
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}

    if all_data.get(directory):
        print("Directory already in output, exiting")
        return
    else:
        all_data.update(wrapped_data)
        with open(output_path, "w") as json_file:
            json.dump(all_data, json_file, indent=4)


def integrity_check_directory(directory_check, older_data):

    directory_check_hash = compute_hash_directory(directory_check)
    new_keys = set(directory_check_hash.keys())
    old_keys = set(older_data.keys())

    added = new_keys - old_keys
    removed = old_keys - new_keys

    modified = {key for key in old_keys & new_keys if older_data[key] != directory_check_hash[key]}
    
    return added,removed,modified


def main():
    if len(sys.argv) != 3:
        print("Usage: ./integrity-check.py <option> <directory>")
        sys.exit()
    option = sys.argv[1]
    directory = sys.argv[2]
    if not valid_directory(directory):
        print("Please enter a valid directory next time")
        sys.exit()

    if option == "baseline":
        data = compute_hash_directory(directory)
        append_to_file(directory, data)
    elif option == "check":        
        baseline_file = os.path.join(BASE_DIR, BASE_FILE)
        with open(baseline_file, "r") as json_file:
            entire_data = json.load(json_file)
            baseline = entire_data.get(directory)
            if baseline is None:
                print("No baseline found for this directory.")
                sys.exit()
            added,removed,modified = integrity_check_directory(directory, baseline)

            if added:
                print(f"Files added: {added}")
            else:
                print("No files added")
            
            if removed:
                print(f"Files Removed: {removed}")
            else:
                print("No files removed")
            
            if modified:
                print(f"Files modified: {modified}")
            else:
                print("No files modified")
    else:
        print("Invalid options")
        sys.exit()



if __name__=="__main__":
    main()