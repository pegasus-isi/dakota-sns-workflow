#!/usr/bin/bash

set -e

inputFile=""
outputFile=""
stdoutFile=""

while getopts ":i:o:s:" opt; do
   case $opt in
      i)
         inputFile="$OPTARG"
         ;;
      o)
         outputFile="$OPTARG"
         ;;
      s)
         stdoutFile="$OPTARG"
         ;;
      \?)
         echo "Invalid option: -$OPTARG" >&2
         exit 1
         ;;
      :)
         echo "Option -$OPTARG requires an argument." >&2
         exit 1
         ;;
   esac
done

if [ -z "$inputFile" ]; then
   echo "You need to provide an input file using the -i argument"
   exit 1
elif [ -z "$outputFile" ]; then
   echo "You need to provide an output file using the -o argument"
   exit 1
elif [ -z "$stdoutFile" ]; then
   stdoutFile="${outputFile%%.*}.stdout"
fi

export PATH="/opt/dakota/6.6.0/bin:/opt/dakota/6.6.0/test:/opt/Mantid/bin:$PATH"
export PYTHONPATH="/opt/dakota/6.6.0/share/dakota/Python:/opt/Mantid/bin:$PYTHONPATH"

dakota -i $inputFile -o $outputFile > $stdoutFile

exit 0

