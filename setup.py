from setuptools import setup

setup(name='actcrm-python',
      version='0.1',
      description='API wrapper for Act! CRM written in Python',
      url='https://github.com/GearPlug/actcrm-python',
      author='Gustavo Saavedra',
      author_email='tavito.286@gmail.com',
      license='GPL',
      packages=['actcrm', ],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
