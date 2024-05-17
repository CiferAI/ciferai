from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cifer",
    version="0.0.1",
    author="cifer.ai",
    author_email="parit@cifer.ai",
    description="Some description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CiferAI/ciferai.git",
    license="MIT",
    packages=find_packages(),
    package_dir={'client': 'Client'},
    install_requires=[
        'requests'
    ],
    tests_require=[
        'coverage', 'wheel', 'pytest', 'requests_mock'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Apache-2.0",
        "Development Status :: 3 - Alpha"
    ]
)