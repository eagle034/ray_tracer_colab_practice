import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()


setuptools.setup(
    name='cython_colab',
    version='0.1',
    author='Chunpo Wang',
    author_email='artoowang@gmail.com',
    description='Cython Colab Utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/artoowang/ray-tracer-colab',
    license='GNU General Public License v3 (GPLv3)',
    # This is needed for single module without a package (directory).
    # See https://docs.python.org/3/distutils/examples.html#pure-python-distribution-by-module
    py_modules=['cython_colab'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Operating System :: OS Independent',
    ],
)
