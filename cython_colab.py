import glob
import importlib.util
import os
import re
import subprocess
from typing import Tuple

def _extract_reload_number(ext_path: str) -> int:
  """Returns the reload number of the given extension path.

  E.g.,
  _extract_reload_number('/usr/local/lib/python3.7/dist-packages/helloworld.reload6.so')
  returns 6.
  """
  result = re.search(r'\.reload([0-9]*)\.so', ext_path)
  if not result:
    raise ValueError(
        f'Failed to extract reload number from the extension path: {ext_path}')
  return int(result[1])


def _find_latest_reload_extension(ext_name: str) -> Tuple[int, str]:
  """Returns the reload number and path of the latest extension |ext_name|.

  Returns (reload number, extension path) tuple.
  """
  reload_module_paths = glob.glob(f'{ext_name}.reload*.so')
  if len(reload_module_paths) == 0:
    return (0, None)
  reload_number_modules = [(_extract_reload_number(module_path), module_path)
                           for module_path in reload_module_paths]
  return max(reload_number_modules)


def _build(setup_path, ext_name=None):
  """Builds the extension with the given setup file path and extension name.

  Args:
    setup_path: The path to a Python file for the Python extension setup.
    ext_name: Optional. When given, it is used as the Python extension name.
      Otherwise, the extension name is derived from the setup Python file path
      with the pattern {ext_name}_setup.py. It is assumed that the setup file is
      configured to create a extension with this name.

  Returns:
    The path to the new, renamed extension with reload<N>, where N is a new
    reload number above all the existing reload extensions.
    E.g., if we already have helloworld.reload6.so and helloworld.reload7.so,
    then this will build helloworld.reload8.so and returns the path to it.
  """
  # Extract extension name from |setup_path|.
  result = re.match(r'(.*/)?([^/]+)_setup.py', setup_path)
  if result:
    ext_name = result[2]
  print(f'Build extension {ext_name} ...')

  next_reload_number = _find_latest_reload_extension(ext_name)[0] + 1
  print(f'Next reload number: {next_reload_number}')

  # Use build_ext --inplace to build the extension in the working directory.
  # Use Popen() instead of just call(), because we need to parse STDOUT and
  # STDERR and explicitly print the result for Colab. Otherwise, Colab will
  # not capture those outputs in the notebook.
  with subprocess.Popen(['python', setup_path, 'build_ext', '--inplace'],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
      print(line, end='')
    print(f'Build exit code: {p.poll()}')

  new_module_path = glob.glob(f'{ext_name}.cpython-*.so')
  if len(new_module_path) < 1:
    raise ValueError(f'Failed to create extension.')
  elif len(new_module_path) > 1:
    print(f'Found multiple created extensions: {new_module_path}. Will use the '
          'first one.')
  new_module_path = new_module_path[0]

  new_reload_module_path = f'{ext_name}.reload{next_reload_number}.so'
  os.rename(new_module_path, new_reload_module_path)
  if not os.path.exists(new_reload_module_path):
    raise ValueError(f'Failed to rename extension to {new_reload_module_path}')
  return new_reload_module_path


def _reload_extension(ext_name: str):
  """Reloads the extension |ext_name|.

  Returns the reloaded extension.
  """
  _, ext_path = _find_latest_reload_extension(ext_name)
  if not ext_path:
    raise ValueError(f'Cannot find extension {ext_name}.') 
  print(f'Loading extension {ext_path} ...')
  spec = importlib.util.spec_from_file_location(ext_name, ext_path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module

def build_extension(ext_name: str):
  """Builds the extension |ext_name|.

  Returns the newly built extension.
  """
  _build(f'{ext_name}_setup.py')
  return _reload_extension(ext_name)
