'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more

-e . in requirements is responsible for triggering setup.py file to
automatically create our project as a package

When the package is being built, to make sure that all the dependencies 
are installed we need to pass requirements as list to install_requires

'''

## find packages scans through entire project folder and where-ever it finds 
## __init__.py file it considers it as a package

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return
    list of requirements
    """
    requirements_lst : List[str] = []
    with open("requirements.txt",'r') as file:
        #Read lines from file
        lines = file.readlines()
        for line in lines:
            requirements = line.strip()
            ## ignore empty lines and -e.
            if requirements != '' and requirements != "-e .":
                requirements_lst.append(requirements)
    return requirements_lst

setup(
    name = "NetworkSecurity",
    version="0.0.1",
    author = "Manas Agarwal",
    author_email="manasmrt10@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()   
)
            