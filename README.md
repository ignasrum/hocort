# HoCoRT
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/hocort/README.html) <br>
<strong>Ho</strong>st <strong>Co</strong>ntamination <strong>R</strong>emoval <strong>T</strong>ool (<strong>HoCoRT</strong>)

Host contamination removal from high-throughput sequencing reads for Linux and Mac OS.

Supports un-/paired FastQ input. Outputs in FastQ format.

# Dependencies
Python 3.7+ <br>
External programs:
* [Bowtie2](https://github.com/BenLangmead/bowtie2) (Tested with version 2.4.5)
* [HISAT2](https://github.com/DaehwanKimLab/hisat2) (Tested with version 2.2.1)
* [Kraken2](https://github.com/DerrickWood/kraken2) (Tested with version 2.1.2)
* [bwa-mem2](https://github.com/bwa-mem2/bwa-mem2) (Tested with version 2.2.1)
* [BBMap](https://sourceforge.net/projects/bbmap/) (Tested with version 38.96)
* [Minimap2](https://github.com/lh3/minimap2) (Tested with version 2.24)
* [samtools](https://github.com/samtools/samtools) (Tested with version 1.15)

# Installing with bioconda

Install with bioconda:
```
conda install -c bioconda hocort
```

# Manual Installation
First ensure that there is no conda environment called "hocort". <br>
Now download the necessary files:
```
wget https://raw.githubusercontent.com/ignasrum/hocort/main/install.sh && wget https://raw.githubusercontent.com/ignasrum/hocort/main/environment.yml
```

After downloading the files, run the installation bash script to install HoCoRT:
```
chmod +x install.sh && ./install.sh
```

The installation is done. Activate the Conda environment:
```
conda activate hocort
```

# Using HoCoRT
### Building indexes
Indexes are required to map sequences, and may be built either manually or with "hocort index" which simplifies the process.
A Bowtie2 index may built using "hocort index" with the following command:
```
hocort index Bowtie2 --input genome.fasta --output dir/basename
```
If one wishes to remove multiple organisms from sequencing reads, the input fasta should contain multiple genomes.
```
cat genome1.fasta genome2.fasta > combined.fasta
```

### Paired end run
To map reads and output mapped/unmapped reads use the following command:
```
hocort map Bowtie2 -x dir/basename -i input1.fastq input2.fastq -o out1.fastq out2.fastq
```

### Single end run
Exactly as above, but with one input file and one output file.
```
hocort map Bowtie2 -x dir/basename -i input1.fastq -o out1.fastq
```

### Removing host contamination
The filter "--filter True/False" argument may be used to switch between outputting mapped/unmapped sequences.
For example, if the reads are contaminated with human sequences and the index was built with the human genome, use "--filter True" to output unmapped sequences (everything except the human reads).

### Extracting specific sequences
The filter "--filter True/False" argument may also be used to extract specific sequences.
First, the index should be built with the genomes of the organisms to extract.
Second, the sequencing reads should be mapped with the "--filter False" argument to output only the mapped sequences (sequences which map to the index containing genomes of the specific organisms).

# Wiki
[Wiki Homepage](https://github.com/ignasrum/hocort/wiki)
