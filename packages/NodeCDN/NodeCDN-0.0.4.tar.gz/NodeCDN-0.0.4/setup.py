from setuptools import setup, find_packages

setup(
    name="NodeCDN",
    version="0.0.4",
    description="NodeCDN for Python.",
    long_description=" Original GitHub repository here: [git](https://github.com/WWEMGamer2/NodeCDN)",
    author="Eric",
    author_email="justaneric.c@gmail.com",
    packages=find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    entry_points = '''
    [console_scripts]
    nodecdn=NodeCDN:nodecdncli
    ''',
    install_requires = ['click']
)