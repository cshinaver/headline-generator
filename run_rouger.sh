#!/bin/bash

usage() {
    cat <<EOF
    Usage: ./run_rouger.sh [-d N] [-t N]

    -d N    Number of dev documents
    -t N    Number of train documents
EOF
    exit 0
}

run_rouge() {
    cd rouge || exit
    java -jar rouge2.0_0.2.jar
}

if ! [ $# -eq 4 ]; then
    usage
fi


while getopts "hd:t:" arg; do
    case $arg in
        h) usage;;
        d) DEV_DOCUMENTS=$OPTARG;;
        t) TRAIN_DOCUMENTS=$OPTARG;;
        *) usage ;;
    esac
done

echo "Removing existing summaries..."
rm rouge/rouge-eval/system/*
echo "Creating summaries..."
python headline.py train.json dev.json "$TRAIN_DOCUMENTS" "$DEV_DOCUMENTS"
echo "Running rouge..."
run_rouge |
grep 'Average' |
awk '{ print $6 }' |
awk -F: '{ print $2 }' |
perl -ne '$i += 1; $sum += $_; END { print $sum/$i . "\n" }'
