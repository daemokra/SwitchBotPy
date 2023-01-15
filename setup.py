from setuptools import setup, find_packages
from switchbotpy import __version__

install_reqs = [
    'certifi>=2022.12.7',
    'charset-normalizer>=2.1.1',
    'idna>=3.4',
    'requests>=2.28.1',
    'urllib3>=1.26.13',
]

setup(
    name='SwitchBotPy',
    version=__version__,
    license='MIT',
    packages=find_packages(),
    install_requires=install_reqs
)