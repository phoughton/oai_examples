import os


def choose_a_file(folder, file_type, prompt):
    """
    This function will list the files in the folder provided and ask the user to choose one of them by number.
    It will then return the contents of that file as a string.
    """
    print(prompt)
    # Create a numbered list the results files in the input folder and ask the user to choose one of them by number
    files = os.listdir(folder)
    files = [file for file in files if file.endswith(file_type)]
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")

    # let user choose the test results file and then read the contents of that file into a variable called test_results
    file_number = input(f"Choose the {file_type} file you want by number:")
    file_number = int(file_number) - 1

    file_contents = open(f"{folder}/{files[file_number]}", "r").read()
    return file_contents
