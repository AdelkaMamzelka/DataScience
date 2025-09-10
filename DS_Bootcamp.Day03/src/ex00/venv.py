#!/usr/bin/env python3

import os

def main():
    current_env = os.getenv('VIRTUAL_ENV')
    if current_env:
        print(f'Your current virtual env is {current_env}')
    else:
        print('No virtual environment is currently activated.')

if __name__ == '__main__':
    main()

#brew install virtualenv
#virtualenv lemonkyl
#source lemonkyl/bin/activate
#фигачим скрипт построчно после ввода "пайтон"
#python3 python3 venv.py для проверки
#выйти из виртуального окружения deactivate
#выйти exit