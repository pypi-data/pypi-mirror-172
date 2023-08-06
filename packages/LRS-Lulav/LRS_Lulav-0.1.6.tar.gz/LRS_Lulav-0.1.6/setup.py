from setuptools import setup

setup(
    name='LRS_Lulav',
    version='0.1.6',
    author='vovacooper',
    author_email='vova@lulav.com',
    packages=[
        'LRS_Lulav',
        'LRS_Lulav.modules'
    ],
    # scripts=[
    #     'bin/script1', 
    #     'bin/script2'
    # ],
    url='http://pypi.python.org/pypi/LRS/',
    license='LICENSE.txt',
    description='LRS_Lulav ',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.1.1",
        "pytest",
        "pymongo",
        "pysqlite3",
        "redis"  ,
        "soupsieve",
        "bs4"     
    ],
)
