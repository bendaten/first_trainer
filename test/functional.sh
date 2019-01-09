#!/usr/bin/env bash

proj=~/PycharmProjects/first_trainer/
source ${proj}venv/bin/activate
export FIRST_TRAINER=${proj}

python ${FIRST_TRAINER}src/main.py --target_time="4:00:00" --race_date="05/05/2018" --race_name="test" --output="text, json"
if [[ "$?" -ne 0 ]]; then
    echo "Trainer failed"
    exit 1
else
    echo "Trainer OK"
fi

output_file=~/Downloads/2018-05-05test.txt
ref_file=${FIRST_TRAINER}test/resources/2018-05-05test.txt
diff ${output_file} ${ref_file}
if [[ "$?" -ne 0 ]]; then
    echo "text format different than reference"
    exit 1
else
    echo "text format output OK"
fi

output_file=~/Downloads/2018-05-05test.json
ref_file=${FIRST_TRAINER}test/resources/2018-05-05test.json
diff ${output_file} ${ref_file}
if [[ "$?" -ne 0 ]]; then
    echo "json format different than reference"
    exit 1
else
    echo "json format output OK"
fi
