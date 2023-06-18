import os
import csv
import sqlite3
from typing import Iterator

def combine_csv_files(file_paths, output_filename):
    combined_data = []
    header = None

    for file_path in file_paths:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
            if header is None:
                header = data[0]
                combined_data.append(header)
            combined_data.extend(data[1:])

    with open(output_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(combined_data)

    print(f"Combined CSV files saved as {output_filename}")

def get_ports(xml_path: str) -> Iterator[list]:
    """
    Retrieves port data from an nmap xml.
    """
    pass

def list_files(file_path: str) -> set[str]:
    """
    Retrieves absolute path(s) for a given file or directory of xml files.
    """
    if os.path.isfile(file_path):
        return set(os.path.abspath(file_path))
    else:
        return set([
            os.path.abspath(f) 
            for f in os.listdir(file_path)
            if f.lower().endswith('.xml')
        ])

if __name__ == '__main__':
    file_paths = set()
    while True:
        file_path = input("Enter the path of the XML file or directory to combine (or 'done' to finish): ")
        if file_path.lower() == 'done':
            break
        if not os.path.exists(file_path):
            print("File/dir not found. Please enter a valid file path.")
            continue
        file_paths |= list_files(file_path)

    output_filename = input("Enter the filename for the combined CSV file: ")
    combine_csv_files(file_paths, output_filename)
