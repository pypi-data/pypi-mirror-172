from setuptools import find_packages, setup
from typing import List 

with open("README.md","r") as fp:
    long_description = fp.read()
    

FILE_OPEN = "requirements.txt"


def get_install_requirements()->List[str]:
    file1 = open(FILE_OPEN,"r")
    requirement_list = file1.readlines()
    requirement_list_str = str("".join(requirement_list))
    requirement_list = requirement_list_str.splitlines()
    requirement_list = [req for req in requirement_list if "-e ." not in req]
    file1.close()
    
    return requirement_list

setup(
    name = "helloworld-vinayak",
    version = "0.0.0",
    description="say hello",
    py_modules=['helloworld'],
    package_dir={'':'src'},
    classifiers=["Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+) ",
                 "Operating System :: OS Independent",
         
                 
                 ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires = [get_install_requirements()],
    
    
    
)