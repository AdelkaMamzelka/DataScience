#!/usr/bin/env python3

import sys

def main():
    clients = [
        'andrew@gmail.com', 'jessica@gmail.com', 
        'ted@mosby.com', 'john@snow.is', 'bill_gates@live.com', 
        'mark@facebook.com', 'elon@paypal.com', 'jessica@gmail.com'
    ]
    participants = [
        'walter@heisenberg.com', 'vasily@mail.ru',
        'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
        'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com'
    ]
    recipients = [
        'andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is'
    ]

    if len(sys.argv) != 2:
        if len(sys.argv) == 1:
            print("Используйте аргумент 'call_center', 'potential_clients', или 'loly_program'!")
            exit(1)
        else:
            raise ValueError("Пожалуйста, используйте не более одного аргумента!")
    else:
        task = sys.argv[1]

    if task == 'call_center':
        result = get_clients(clients, recipients, None)
        print("Клиенты, которые не просмотрели рекламное письмо:")
        print('\n'.join(result))

    elif task == 'potential_clients':
        result = get_non_clients(participants, clients, None)
        print("Люди, которые не являются вашими клиентами:")
        print('\n'.join(result))

    elif task == 'loly_program':
        result = dnparticipate_event(clients, participants, None)
        print("Клиенты, которые не участвовали в мероприятии:")
        print('\n'.join(result))

    else:
        raise ValueError("Неверные данные. Пожалуйста, используйте 'call_center', 'potential_clients', or 'loly_program'!")

def get_clients(clients, recipients, task):
    clients_set = set(clients)
    recipients_set = set(recipients)
    return list(clients_set - recipients_set)

def get_non_clients(participants, clients, task):
    participants_set = set(participants)
    clients_set = set(clients)
    return list(participants_set - clients_set)

def dnparticipate_event(clients, participants, task):
    clients_set = set(clients)
    participants_set = set(participants)
    return list(clients_set - participants_set)

if __name__ == "__main__":
    main()
    