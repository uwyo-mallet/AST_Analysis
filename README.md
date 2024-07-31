July 2024

University of Wyoming, College of Engineering
Lars Kotthoff
Grace Abawe

Python scripts for extracting graph characteristics from Abstract Syntax Trees

Ensure that the imported modules are installed and that the python virtual environment is activated.

For C code:
Then, to build the ASTs, extract characteristics, and visualize, run the following:

    python3 ast_analysis.py  <sourcefiles.c>

Multiple file paths can be specificied, it will prompt you for wether you would like to visualize graphs, and the output will be saved in 'c_results.csv'.

--------------------------------------------------------------------------------------------------------------------

For python code:
To build the ASTs, extract characteristics, and visualize, run the following:

    python3 python_ast_analysis.py <sourcefiles.py> 

Multiple file paths can be specificied, it will prompt you for wether you would like to visualize graphs, and the output will be saved in 'p_results.csv'.

---------------------------------------------------------------------------------------------------------------------

Example code files have been included in the ast_analysis folder, such as simple.c, matrix.c, and simple.py

Common issues:
If experiencing issues with uninstalled modules, try running:
    pip install networkx matplotlib
    sudo apt-get install graphviz

Tutorial for creating and activating a virtual environment:
    https://python.land/virtual-environments/virtualenv
