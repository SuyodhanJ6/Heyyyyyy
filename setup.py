from setuptools import find_packages, setup
from typing import List
def get_requirements()->list(str):
    """
    Method Name : get_requirements
    Description : This function returns a list of requirements.
    Revision    : 0.0.1
    On Failure  : None
    OutPut      : List[str]
    """
    with open('requirements.txt', 'r') as file:
        requirments_list:List[str] = file.readlines()
    requirments_list = [requirement.strip() for requirement in requirments_list]

    return requirments_list
    
setup(
    name = 'sensorcloud',
    version= '0.0.1',
    author='Prashant',
    author_email='prashant@sensorcloud.com',
    packages=find_packages(),
    install_requires = ["pymongo==4.2.0"],

)

