#!/bin/bash

file_exists () {
	if [ -f "$1" ]; then
		echo $1
		return 0;
	else
		return 1;
	fi
}

dir_exists () {
	if [ -d "$1" ]; then
		echo $1
		return 0;
	else
		return 1;
	fi
}

if ! file_exists "SRR3733117.1.fastq" ; then
	wget -nc https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos1/sra-pub-run-1/SRR3733117/SRR3733117.1;
	fasterq-dump SRR3733117.1;
	rm SRR3733117.1;
fi

if ! dir_exists "bowtie2" ; then
	wget -nc https://genome-idx.s3.amazonaws.com/bt/grch38_1kgmaj_snvindels_bt2.zip;
	mkdir bowtie2;
	unzip grch38_1kgmaj_snvindels_bt2.zip -d bowtie2;
	rm -f grch38_1kgmaj_snvindels_bt2.zip;
fi
