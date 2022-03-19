import logging

import hocort.execute as exe

logger = logging.getLogger(__file__)


external_dependencies = {
    'bowtie2': ['bowtie2'],
    'kraken2': ['kraken2'],
    'hisat2': ['hisat2'],
    'bwa-mem2': ['bwa-mem2'],
    'bbmap': ['bbmap.sh'],
    'minimap2': ['minimap2'],
    'samtools': ['samtools']
}


def check_external_dependencies():
    """
    Checks for external dependencies.

    Returns
    -------
    result : bool
        True if all external dependencies are present,
        False if any of the external dependencies are not present.

    """
    result = True
    for dependency in external_dependencies:
        try:
            cmd = external_dependencies[dependency]
            returncodes = exe.execute(cmd)
            logger.info(f'{dependency} is installed.')
        except FileNotFoundError as fe:
            logger.error(f'{dependency} is not installed: {fe}')
            result = False
    return result
