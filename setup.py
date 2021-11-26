import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()


setuptools.setup(
    name='cython_colab',
    version='0.1',
    scripts=['cython_colab.py'] ,
    author='Chunpo Wang',
    author_email='artoowang@gmail.com',
    description='Cython Colab Utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/artoowang/ray-tracer-colab',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Operating System :: OS Independent',
    ],
)
