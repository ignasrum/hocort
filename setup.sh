conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda install bowtie2 minimap2 bwa-mem2 hisat2 pysam samtools bedtools seqtk htslib sra-tools vsearch
conda install -c agbiome bbtools insilicoseq
