from setuptools import setup, find_packages

install_reqs = [
    'certifi==2022.12.7',
    'charset-normalizer==2.1.1',
    'idna==3.4',
    'python-dotenv==0.21.0',
    'requests==2.28.1',
    'urllib3==1.26.13',
]

setup(
    name='SwitchBotPy',
    version='0.1',
    license='MIT',
    packages=find_packages(),
    install_requires=install_reqs
)