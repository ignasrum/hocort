conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda install seqtk sra-tools vsearch insilicoseq art htslib seqkit fastx_toolkit emboss sga cutadapt mummer4 recentrifuge
conda install -c agbiome bbtools

conda install -c pysam samtools bowtie2 minimap2 bwa-mem2 hisat2 kraken2 star bbmap #centrifuge
