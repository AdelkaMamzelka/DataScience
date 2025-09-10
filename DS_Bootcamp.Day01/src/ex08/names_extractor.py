#!/usr/bin/env python3

import sys

def process_email(email):
    name_part = email.split('@')[0]  
    name, surname = name_part.split('.') 
    return name.capitalize(), surname.capitalize(), email

def main():
    if len(sys.argv) != 2:
        print("Используйте: ./names_extractor.py path_to_email_file.txt")
        return
    
    email_file_path = sys.argv[1]
    try:
        with open(email_file_path, 'r') as file:
            email_addresses = file.read().strip().split('\n')
        
        employees = []
        
        for email in email_addresses:
            if email.strip(): 
                name, surname, email = process_email(email.strip())
                employees.append((name, surname, email))
        
        with open('employees.tsv', 'w') as output_file:
            line_number = 1  
            
            output_file.write(f"{line_number}\tA\tB\tC\n")  
            line_number += 1
            
            output_file.write(f"{line_number}\tName\tSurname\tE-mail\n") 
            line_number += 1
            
            for name, surname, email in employees:
                output_file.write(f"{line_number}\t{name}\t{surname}\t{email}\n")
                line_number += 1
        
        print("Данные успешно записаны в файл employees.tsv.")

    except FileNotFoundError:
        print(f"Файл {email_file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()