from setuptools import setup, find_packages

setup(
    name="AmazonParser",
    version="0.1.2",
    author="Ali Najafi",
    author_email="mail.ali.najafi@gmail.com",
    description="A Parser for Amazon Pages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/a4fr/AmazonParser",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'lxml'
    ],
    entry_points={
        'console_scripts': [
            'amazonparser=amazonparser.cli:main',
        ],
    },
)
