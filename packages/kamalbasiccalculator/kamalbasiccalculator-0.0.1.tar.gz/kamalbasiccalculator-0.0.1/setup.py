from setuptools import setup,find_packages

classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

setup(
    name='kamalbasiccalculator',
    version='0.0.1',
    description='A simple calculator with basic operations',
    Long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='Kamal K',
    author_email='krajakk6@gmail.com',
    licence='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
    )

