#!/usr/bin/env python3

def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_tsv(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(data)

def convert_csv_to_tsv(input_file, output_file):
    csv_data = read_csv(input_file)
    
    tsv_data = []
    for line in csv_data:
        elements = []
        current_element = []
        in_quotes = False

        for char in line:
            if char == '"':
                in_quotes = not in_quotes

            if char == ',' and not in_quotes:
                elements.append(''.join(current_element))
                current_element = []
            else:
                current_element.append(char)

        elements.append(''.join(current_element))
        
        tsv_line = '\t'.join(elements) + '\n'
        tsv_data.append(tsv_line)

    write_tsv(output_file, tsv_data)


if __name__ == "__main__":
    input_file = 'ds.csv'  
    output_file = 'ds.tsv'  
    convert_csv_to_tsv(input_file, output_file)  