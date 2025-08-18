import os


def clean_up_files(inter_files):
    for file in inter_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"File: {file} deleted successfully")
        else:
            print(f"File: {file} does not exist")
