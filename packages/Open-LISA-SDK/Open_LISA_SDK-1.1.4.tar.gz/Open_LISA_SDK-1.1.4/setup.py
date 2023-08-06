
from pathlib import Path
from setuptools import setup, find_packages

VERSION_PLACEHOLDER = '1.1.4'

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='Open_LISA_SDK',         # How you named your package folder (MyLib)
    packages=find_packages(),
    # Start with a small number and increase it with every change you make
    version=VERSION_PLACEHOLDER,
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='SDK for Laboratory Instrument Station Adapter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ariel Alvarez Windey & Gabriel Robles',                   # Type in your name
    author_email='ajalvarez@fi.uba.ar',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/aalvarezwindey/Open-LISA-SDK',
    readme='https://github.com/aalvarezwindey/Open-LISA-SDK/README.md',
    download_url='https://github.com/aalvarezwindey/Open-LISA-SDK/archive/refs/tags/{}.tar.gz'.format(
        VERSION_PLACEHOLDER),
    keywords=['SDK', 'ELECTRONIC', 'INSTRUMENT', 'ADAPTER', 'FIUBA', 'OPEN',
              'LISA', 'LABORATORY'],   # Keywords that define your package best
    install_requires=["pyserial"],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
    ],
)
