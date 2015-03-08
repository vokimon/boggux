#!/bin/bash

lang=${1:-ca}
echo Generating ${lang} dictionary
aspell -l $lang dump master |
aspell -l $lang expand |
while read line
do
	for a in $line
	do
		echo $a
	done
done |
grep -v "[-'A-Z]" > wordlist.${lang}.dict
