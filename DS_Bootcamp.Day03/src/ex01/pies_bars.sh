#!/bin/bash

# Создаем файл с данными
cat << EOF > data.txt
2007 73.32 70.52
2008 81.23 93.00
2009 181.43 135.10
2010 110.21 95.00
2011 93.97 90.45
EOF

# Генерируем график
termgraph data.txt --title "Pies and Bars" --bars --color magenta cyan --no-legend

#сначала устанавливаем нужную библиотеку pip3 install termgraph
#пишем в терминале termgraph data.txt --title "Pies and Bars" --color magenta cyan
