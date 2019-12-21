# CMGL: Context-Manager-based OpenGL for Python

[![Build Status](https://travis-ci.org/fofix/python-cmgl.svg?branch=master)](https://travis-ci.org/fofix/python-cmgl)


CMGL is a C-extension in Python. This is a Python binding for OpenGL that uses
context managers.


## Setup

### Dependencies

You'll need those packages:

* `OpenGL`
* `numpy`.


### Native modules

Build the extension:

    python setup.py build_ext --inplace --force
