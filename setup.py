from setuptools import setup

setup(
    name='hocort',
    version='0.1.0',
    description='Host Contamination Removal Tool',
    url='https://github.com/ignasrum/hocort',
    author='Ignas Rumbavicius',
    license='MIT',
    packages=['hocort',
              'hocort.aligners',
              'hocort.pipelines',
              'hocort.parse'],
    python_requires='>=3.8',
    install_requires=['argparse',
                      'pytest'],
    entry_points = {
        'console_scripts': ['hocort=hocort.__main__:main',
                            'hocort-compare=hocort.compare:main'],
    }
)
