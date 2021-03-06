# coding=utf-8

import io
import os
import re
import sys
from setuptools import setup, find_packages

# Integrated libraries - add them to the system path (needed for running tests)
# Insert libs that are only needed for certain python versions
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)
if PY34:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'libpy34')))
elif PY3:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'libpy3')))
elif PY2:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'libpy2')))
else:
    pass
# Insert common libs for all python versions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

# Root path
root_path = os.path.abspath(os.path.dirname(__file__))

# Version (version must be compliant with version.StrictVersion of distutils)
with io.open(os.path.join(root_path, 'autosubliminal', 'version.py'), 'r') as f:
    version = re.search(r'^RELEASE_VERSION\s*=\s*[\'\"]((\d+)\.(\d+)(\.(\d+))?([ab](\d+))?)[\'\"]$', f.read(),
                        re.MULTILINE).group(1)

# Readme
with io.open(os.path.join(root_path, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

# Requirements
setup_requirements = ['pytest-runner'] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else []

install_requirements = []

test_requirements = ['pytest', 'pytest-mock', 'pytest-pep8', 'pytest-flakes', 'requests-mock', 'vcrpy']

dev_requirements = ['tox']

# Setup
setup(name='Auto-Subliminal',
      version=version,
      license='GPL v3',
      description='Auto-Subliminal, the automated subliminal subtitle downloader',
      long_description=readme,
      keywords='subtitle subtitles video movie episode tv show',
      url='https://github.com/h3llrais3r/Auto-Subliminal',
      author='h3llrais3r',
      author_email='pooh_beer_1@hotmail.com',
      packages=find_packages(),
      setup_requires=setup_requirements,
      install_requires=install_requirements,
      tests_require=test_requirements,
      extras_require={
          'test': test_requirements,
          'dev': dev_requirements
      })
