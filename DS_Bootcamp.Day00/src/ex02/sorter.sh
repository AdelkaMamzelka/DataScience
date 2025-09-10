#!/bin/sh

{
    cat ../ex01/hh.csv | head -n 1  # Заголовок
    cat ../ex01/hh.csv | tail -n +2 | sort -t',' -k2 -k1  # Сортировка по 'created_at' и 'id'
} > hh_sorted.csv

echo "Сортировка завершена. Результат сохранен в hh_sorted.csv."