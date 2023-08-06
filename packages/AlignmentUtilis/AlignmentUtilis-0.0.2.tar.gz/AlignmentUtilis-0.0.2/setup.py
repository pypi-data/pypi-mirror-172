from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='AlignmentUtilis',
    version='0.0.2',
    description='Simple application of sequence alignment algorithms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Youpu-Chen/Myscripts/tree/main/Sequence_Handle/sequencealignment',
    download_url='',
    author='Youpu Chen',
    author_email='otis.hongpu@gmail.com',
    license='MIT',
    install_requires=['numpy', 'matplotlib'],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Information Technology',
    'Topic :: Scientific/Engineering :: Bio-Informatics',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
  ]
)