#!/bin/sh

rm -rf hh.csv

echo "\"id\", \"created_at\", \"name\", \"has_test\", \"alternate_url\"" > hh.csv

jq -r -f filter.jq ../ex00/hh.json >> hh.csv

echo "Данные успешно преобразованы в hh.csv."