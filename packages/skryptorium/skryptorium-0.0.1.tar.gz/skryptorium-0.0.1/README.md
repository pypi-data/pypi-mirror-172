skryptorium
===========

Tools for working with single-cell DNA sequencing data


Usage (CLI)
-----------

    skryptorium


Usage (API)
-----------

    from skryptorium import hello
    
    print(hello.hello())


Development
-----------

Set up and activate virtual environment

    # Create `venv` and install IPython and twine
    0/make_venv.sh
    venv/bin/activate

    # Install skryptorium package in editable mode
    0/run_pip_installe.sh

Run IPython for testing with `autoreload`

    ipython
    %load_ext autoreload
    %autoreload 2 
