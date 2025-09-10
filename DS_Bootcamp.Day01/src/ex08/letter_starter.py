#!/usr/bin/env python3

import sys

def find_employee(email, employees_file):
    with open(employees_file, 'r') as file:
        for line in file:
            number, name, surname, employee_email = line.strip().split('\t')
            if employee_email == email:
                return name, surname
    return None

def generate_email(name, surname, email): #почему так
    employee_name = f"Dear {name}, welcome to our team. " \
                    f"We are sure that it will be a pleasure to work with you. " \
                    f"That’s a precondition for the professionals that our company hires."
    return employee_name

def main():
    if len(sys.argv) != 3:
        print("Используйте: ./letter_starter.py email employees.tsv")
        return
    
    email = sys.argv[1]
    employees_file = sys.argv[2]
    
    employee_data = find_employee(email, employees_file)
    if employee_data is None:
        print("Сотрудника с таким email не найдено.")
        return
    
    employee_name, surname = employee_data
    email_text = generate_email(employee_name, surname, email)
    print(email_text)

if __name__ == "__main__":
    main()