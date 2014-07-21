from setuptools import setup, find_packages
import os

def version(name):
  fname = os.path.join(name, '_version.py')
  environ = {}
  execfile(fname, environ)
  return environ['__version__']


if __name__ == '__main__':
  NAME = 'optim'
  setup(
    name         = NAME,
    version      = version(NAME),
    author       = 'Daniel Duckworth',
    author_email = 'duckworthd@gmail.com',
    description  = 'Reference implementations of optimization algorithms',
    license      = 'BSD',
    keywords     = 'optimization',
    url          = 'http://github.com/duckworthd/optim',
    packages     = find_packages(),
    classifiers  = [
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
    ],
    install_requires = [
      'matplotlib',
      'numpy',
    ],
    tests_require = [
      'nose',
    ]
  )
