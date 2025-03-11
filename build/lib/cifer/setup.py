from setuptools import setup, find_packages

setup(
    name='cifer',
    version='0.1.0',
    description='A Federated Learning WebSocket Server Library with Optional Homomorphic Encryption',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'websockets',
        'numpy',
        'tensorflow',
        'pycryptodome',
        'jwt'
    ],
)
