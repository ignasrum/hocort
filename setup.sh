conda config --add channels defaults
conda config --add channels bioconda
#conda config --add channels conda-forge

conda install -c bioconda pysam samtools bowtie2 minimap2 bwa-mem2 hisat2 kraken2 star bbmap #centrifuge
