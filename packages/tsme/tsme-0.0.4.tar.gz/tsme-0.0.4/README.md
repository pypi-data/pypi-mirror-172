# TSME

A project for estimating differential equations from time series data. Documentation available 
[here](https://nonlinear-physics.zivgitlabpages.uni-muenster.de/ag-kamps/tsme/)

## Install
The package can now be installed with 
```shell
pip install tsme
``` 



## To build
Make sure relevant packages are up-to-date 
```shell
pip install --upgrade setuptools wheel
``` 

Generate distribution files: 
```shell
python setup.py sdist bdist_wheel
``` 

Local install: 
```shell
pip install -e .
``` 

## To publish
Make sure releveant package is installed and up-to-date 
```shell
pip install --upgrade twine
``` 

upload to test repo: 
```shell
python -m twine upload --repository testpypi dist/*
``` 


upload to official repo: 
```shell
python -m twine upload dist/*
``` 

## To build documentation
```shell
tsme/docs$ sphinx-apidoc --force -o source .. ../setup.py
tsme/docs$ sphinx-build . build
``` 



