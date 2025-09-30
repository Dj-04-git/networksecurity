from setuptools import find_packages,setup
from typing import List

def get_requriements()->List[str]:
    """
    This function will return list of requriemnts
    """
    requriements_lst:List[str] = []
    try:
        with open("requirements.txt",'r') as file:
            # read lines from the file
            Lines = file.readlines()
            #process each line 
            for line in Lines:
                requriement = line.strip()
                ## igonre the empty lines and -e .
                if requriement and requriement != '-e .':
                    requriements_lst.append(requriement)
    except FileNotFoundError:
        print("requirements.txt file is not found")
    return requriements_lst

setup(
    name="Network Security",
    version="0.0.1",
    author="Damodar",
    author_email="jadhavdamodar026@gmail.com",
    packages=find_packages(),
    install_requires = get_requriements()
)