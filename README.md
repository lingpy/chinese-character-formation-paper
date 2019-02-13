# Source code and data accompanying the paper ""

## Installation instructions

To install the Python requirements, make sure to have a fresh installation o Python3, ideally in a virtual environment, and then type:

```
$ pip install pip-requirements.txt
```

This should install all packages needed to run the analyses discussed here.

You will also need Pandoc, which we use to convert from HTML to PDF and LaTeX.

## Running the experiments

To run all experiments, type:

```
$ make all
```

And all the code will be executed in order.

Otherwise, you can also run the analyses in separation, here, simply type:

```
$ make ANALYSIS
```

where ANALYSIS is one of `sagart` 
