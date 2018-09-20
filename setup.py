import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='actcrm-python',
      version='0.1.0',
      description='API wrapper for Act! CRM written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/actcrm-python',
      author='Gustavo Saavedra',
      author_email='tavito.286@gmail.com',
      license='GPL',
      packages=['actcrm', ],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
