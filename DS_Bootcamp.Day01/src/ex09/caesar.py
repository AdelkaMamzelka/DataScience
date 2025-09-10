#!/usr/bin/env python3

import sys

def caesar_cipher(text, shift, decode=False):
    result = ""
    if decode:
        shift = -shift
    
    for char in text:
        if char.isalpha():
            #опр базу (ASCII-код 'a' или 'A')
            base = ord('a') if char.islower() else ord('A')
            #прим сдвиг и обрабатываем переполнение
            shifted = (ord(char) - base + shift) % 26 + base
            result += chr(shifted)
        else:
            result += char
    
    return result

def main():
    if len(sys.argv) != 4:
        raise ValueError("Неверное количество аргументов. Используйте: python3 caesar.py encode|decode 'text' shift")
    
    mode = sys.argv[1]
    input_text = sys.argv[2]
    shift = int(sys.argv[3])
    
    #проверка, не содержит ли текст кириллические символы
    if any('\u0400' <= c <= '\u04FF' for c in input_text):
        raise Exception("Скрипт пока не поддерживает ваш язык.")
    
    if mode not in ['encode', 'decode']:
        raise ValueError("Первый аргумент должен быть 'encode' или 'decode'.")
    
    if mode == 'encode':
        print(caesar_cipher(input_text, shift))
    elif mode == 'decode':
        print(caesar_cipher(input_text, shift, decode=True))

if __name__ == "__main__":
    main()