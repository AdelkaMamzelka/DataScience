#!/bin/sh

if [ $# -ne 1 ]; then
    echo "Использование: $0 'название вакансии'"
    exit 1
fi

JOB_TITLE="$(echo $1 | sed 's/ /%20/g')"

URL="https://api.hh.ru/vacancies"

PARAMS="text=${JOB_TITLE}&area=113&per_page=20"

curl -s "${URL}?${PARAMS}" | jq '.' > hh.json

echo "Вакансии по запросу '${JOB_TITLE}' сохранены в файле hh.json."

# brew install jq