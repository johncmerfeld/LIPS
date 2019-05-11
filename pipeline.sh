#!/usr/bin/env bash


mkdir -p wordFiles
mkdir -p vidData
mkdir -p predictions
mkdir -p modelData

set -e

limit="$1"
wordFile="$2"
vidDataFile="$3"
xFile="$4"
yFile="$5"
h="$6"
w="$7"
predFile="$8"

#echo "Creating frequency dictionary..."
#python src/createDictionary.py $files
echo "Creating video data objects..."
python src/splitVideosWithDictionary.py $limit $wordFile $vidDataFile
echo "Transforming video data into model input..."
python src/processVideo.py $vidDataFile $wordFile $xFile $yFile $h $w
echo "Training model..."
python src/model.py $xFile $yFile $predFile $h $w
set +e

