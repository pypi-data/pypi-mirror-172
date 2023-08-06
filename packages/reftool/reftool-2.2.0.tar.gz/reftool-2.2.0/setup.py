import shutil
import setuptools
from pathlib import Path
from setuptools.command.install import install


def copy_config() -> None:
    '''
    Copies the reftool configuration file to ~/.config/reftool.ini

    Parameters:
         None

     Returns:
         None
    '''
    config_dir = Path.home().joinpath('.config')
    config_file = config_dir.joinpath('reftool.ini')
    module_path = Path(__file__).parent

    config_dir.mkdir(exist_ok=True)

    if not config_file.exists():
        shutil.copy(module_path.joinpath('reftool/resources/reftool.ini'), config_file)


class PostInstallCommand(install):
    '''
    Hook to install config file.

    Parameters:
         install

    Returns:
         None
    '''
    def run(self):
        copy_config()
        install.run(self)


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='reftool',
    version='2.2.0',
    url='https://github.com/usdAG/reftool',
    author='Tobias Neitzel (@qtc_de)',
    description='reftool - A commandline interface for accessing reference archives',
    long_description=long_description,
    long_description_content_type='text/markdown',

    packages=['reftool'],
    install_requires=['pyperclip', 'PyYAML'],
    scripts=['bin/ref'],
    package_data={'reftool': ['resources/reftool.ini']},
    cmdclass={'install': PostInstallCommand},
    classifiers=[
                    'Programming Language :: Python :: 3',
                    'Operating System :: Unix',
                    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                ],
)
