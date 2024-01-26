from pathlib import Path


def search_string_in_file(file_path, search_string):
    lines_counter = 0

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            if search_string in line:
                lines_counter += 1

    return lines_counter


desired_string = input("Please, enter the string to search: ")

src_root = Path(__file__).parent
file_path = src_root / "rockyou.txt"

if file_path.is_file():
    lines_found = search_string_in_file(file_path, desired_string)
    print(f"Found in {lines_found} lines in the file.")
else:
    print(f"File '{file_path}' not found. Please make sure the file exists.")
