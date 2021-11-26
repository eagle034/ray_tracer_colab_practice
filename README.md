# Cython Colab Utilities

This Python package contains utility functions to help Cython workflows on
Colab. In particular, it allows building a named Cython module from the given
setup.py, and the ability to rebuild and reload the module without restarting
the Colab runtime.

## Example usage

In Colab, use `%%file` to write out `<module_name>_setup.py` that builds the
Cython module, and run the following:

    module = cython_colab.build_extension('<module_name>')
