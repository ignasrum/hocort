# HoCoRT
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/hocort/README.html)
[![anaconda download page](https://img.shields.io/conda/dn/bioconda/hocort.svg?style=flat)](https://anaconda.org/bioconda/hocort)
<br>
[bioRxiv - HoCoRT: Host contamination removal tool](https://www.biorxiv.org/content/10.1101/2022.11.18.517030v1)
<br>
<strong>Ho</strong>st <strong>Co</strong>ntamination <strong>R</strong>emoval <strong>T</strong>ool (<strong>HoCoRT</strong>)

Removes specific organisms from sequencing reads on Linux and Mac OS.

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

# Installing with Bioconda

To install with Bioconda run the following command:
```
conda install -c bioconda -c conda-forge hocort
```

HoCoRT's dependencies may conflict with existing packages.
This can be solved by installing HoCoRT in a separate environment.
To create a new conda environment and install HoCoRT run the following command:
```
conda create -n hocort -c bioconda -c conda-forge hocort
```

# Manual Installation
First ensure that there is no conda environment called "hocort". <br>
Now download the necessary files:
```
wget https://raw.githubusercontent.com/ignasrum/hocort/main/install.sh && wget https://raw.githubusercontent.com/ignasrum/hocort/main/environment.yml
```

After downloading the files, run the installation bash script to install HoCoRT:
```
bash ./install.sh
```

The installation is done. Activate the Conda environment:
```
conda activate hocort
```

# Using HoCoRT
### Pipeline naming
Pipelines are named after the tools they utilize.
For example, the pipeline bowtie2 uses Bowtie2 to map the reads, and kraken2bowtie2 first classifies using Kraken2, then maps using Bowtie2.

### Building indexes
Indexes are required to map sequences, and may be built either manually or with "hocort index" which simplifies the process.
A Bowtie2 index may built using "hocort index" with the following command:
```
hocort index bowtie2 --input genome.fasta --output dir/basename
```
If one wishes to remove multiple organisms from sequencing reads, the input fasta should contain multiple genomes.
```
cat genome1.fasta genome2.fasta > combined.fasta
```

### Paired end run
To map reads and output mapped/unmapped reads use the following command:
```
hocort map bowtie2 -x dir/basename -i input1.fastq input2.fastq -o out1.fastq out2.fastq
```

### Single end run
Exactly as above, but with one input file and one output file.
```
hocort map bowtie2 -x dir/basename -i input1.fastq -o out1.fastq
```

### Compressed input/output
Most pipelines support .gz compressed input and output.
No extra configuration is required aside from having ".gz" extension in the filename.

### Removing host contamination
The filter "--filter true/false" argument may be used to switch between outputting mapped/unmapped sequences.
For example, if the reads are contaminated with human sequences and the index was built with the human genome, use "--filter true" to output unmapped sequences (everything except the human reads).

### Extracting specific sequences
The filter "--filter true/false" argument may also be used to extract specific sequences.
First, the index should be built with the genomes of the organisms to extract.
Second, the sequencing reads should be mapped with the "--filter false" argument to output only the mapped sequences (sequences which map to the index containing genomes of the specific organisms).

# Advanced usage
### Importing and using HoCoRT in Python
HoCoRT can be imported in Python scripts and programs with "import hocort".
This allows precise configuration of the tools being run.
```
import hocort.pipelines.bowtie2 as bowtie2

idx = "dir/basename"
seq1 = "in1.fastq"
seq2 = "in2.fastq"
out1 = "out1.fastq"
out2 = "out2.fastq"
options = ["--local", "--very-fast-local"] # options is passed to the aligner/mapper, this allows precise configuration

returncode = bowtie2.run(idx, seq1, out1, seq2=seq2, out2=out2, options=options)
```
### Passing arguments to the underlying tools
It is possible to pass arguments to the underlying tools by specifying them in the -c/--config argument like this:
```
hocort map bowtie2 -c="--local --very-fast-local --score-min G,21,9"
```

# Wiki
[Wiki Homepage](https://github.com/ignasrum/hocort/wiki)

# Technical documentation
[https://ignasrum.github.io/hocort/](https://ignasrum.github.io/hocort/)
