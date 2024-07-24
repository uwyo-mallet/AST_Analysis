July 2024

University of Wyoming, College of Engineering
Lars Kotthoff
Grace Abawe

Python scripts for extracting graph characteristics from Abstract Syntax Trees

For C code:
First, generate the AST using Clang by running the following command in your terminal:

    clang -Xclang -ast-dump=json -fsyntax-only <sourcefile.c> > ast.txt


Ensure that the imported modules are installed and that the python virtual environment is activated.
Then, execute the python script to parse and extract characteristics from the AST and visualize it by running the following:

    python3 ast_analysis.py

--------------------------------------------------------------------------------------------------------------------

For python code:
To build the AST, extract characteristics, and visualize, run the following:

    python3 python_ast_analysis.py <sourcefile.py>

---------------------------------------------------------------------------------------------------------------------

Example code files have been included in the ast_analysis folder, such as simple.c, matrix.c, and simple.py

Common issues:
If experiencing issues with uninstalled modules, try running:
    pip install networkx matplotlib
    sudo apt-get install graphviz

Tutorial for creating and activating a virtual environment:
    https://python.land/virtual-environments/virtualenv
