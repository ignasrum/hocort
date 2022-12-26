from setuptools import setup

from hocort.version import __version__


setup(
    name='hocort',
    version=__version__,
    description='Host Contamination Removal Tool',
    url='https://github.com/ignasrum/hocort',
    author='Ignas Rumbavicius',
    license='MIT',
    packages=['hocort',
              'hocort.aligners',
              'hocort.pipelines',
              'hocort.parse'],
    python_requires='>=3.7',
    install_requires=['argparse',
                      'pytest'],
    entry_points = {
        'console_scripts': ['hocort=hocort.__main__:main'],
    }
)
