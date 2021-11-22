conda config --add channels conda-forge 
conda config --add channels bioconda
conda config --set channel_priority flexible 

conda install -c bioconda pysam samtools bowtie2 minimap2 bwa-mem2 hisat2 star bbmap kraken2
