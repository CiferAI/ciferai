from setuptools import setup, find_packages
import os

def read_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return "Description not available."

setup(
    name="cifer",
    version="1.0.7",
    author="Cifer.ai",
    author_email="support@cifer.ai",
    description="Federated Learning and Fully Homomorphic Encryption",
    long_description=read_file("README.md") + "\n\n" + read_file("CHANGELOG.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/cifer-ai/cifer",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tensorflow>=2.0",
        "numpy",
        "flask",  
        "uvicorn",  
        "pydantic",  
        "PyJWT",
        "websockets",
        "argon2-cffi",
        "h11",
        "httpcore",
        "idna",
        "Jinja2",
        "jsonschema",
        "kiwisolver",
        "MarkupSafe",
        "matplotlib-inline",
        "pandas",
        "pillow",
        "prometheus_client",
        "psutil",
        "pycryptodome",
        "Pygments",
        "python-dateutil",
        "pytz",
        "PyYAML",
        "rich",
        "six",
        "sniffio",
        "sympy",
        "torch",
        "torchvision",
        "tornado",
        "tqdm",
        "typer",
        "typing_extensions",
        "tzdata",
        "urllib3",
        "websocket-client",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security :: Cryptography",
        "Framework :: Flask",
    ],
   entry_points={
    'console_scripts': [
        'cifer = cifer.cli:main',
    ],
},


    python_requires=">=3.7",
)
