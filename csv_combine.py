import os
import csv

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

if __name__ == '__main__':
    file_paths = []
    while True:
        file_path = input("Enter the path of the CSV file to combine (or 'done' to finish): ")
        if file_path.lower() == 'done':
            break
        if not os.path.exists(file_path):
            print("File not found. Please enter a valid file path.")
            continue
        file_paths.append(file_path)

    output_filename = input("Enter the filename for the combined CSV file: ")
    combine_csv_files(file_paths, output_filename)
