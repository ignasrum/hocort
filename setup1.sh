conda config --add channels conda-forge 
conda config --add channels bioconda
conda config --set channel_priority flexible 

conda install -c bioconda pysam
conda install -c bioconda samtools
conda install -c bioconda bowtie2
conda install -c bioconda minimap2
conda install -c bioconda bwa-mem2
conda install -c bioconda hisat2
conda install -c bioconda star
conda install -c bioconda bbmap
conda install -c bioconda kraken2
