import __main__
import pkg_resources

from setuptools import setup, Command
import codecs
import re
import os

here = os.path.abspath(os.path.dirname(__file__))

setup(name='stickynotes2modernpaste',
      version='1.0.0',
      description='Web application for bridging between sticky-notes and modernpaste',
      author='Ricky Elrod',
      author_email='relrod@redhat.com',
      license='MIT',
      url='https://github.com/fedora-infra/stickynotes2modernpaste',
      packages=['stickynotes2modernpaste'],
      package_dir={'stickynotes2modernpaste': 'stickynotes2modernpaste'},
      include_package_data=True,
      install_requires=[
          'Flask>=0.9'
      ]
)
