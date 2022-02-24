conda config --add channels conda-forge 
conda config --add channels bioconda
conda config --set channel_priority flexible 

conda install -c bioconda samtools bowtie2 minimap2 bwa-mem2 hisat2 bbmap kraken2
