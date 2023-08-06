from setuptools import setup, find_packages
from distutils.core import setup

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
# setup(
#   name='mycalculator_SD',
#   version='0.0.1',
#   description='This is my first and very basic calculator',
#   long_description="long description" + '\n\n' + open('CHANGELOG.txt').read(),
#   url='',
#   author='Serif Dogru',
#   author_email='dogruserif12@gmail.com',
#   license='MIT',
#   classifiers=classifiers,
#   keywords='calculator, basic',
#   packages=find_packages(),
#   install_requires=['']
# )
from setuptools import setup

with open("README.txt", 'r') as f:
    long_description = f.read()

setup(
   name='mycalculator_SD',
   version='0.1',
   description='A useful calculator module',
   license="MIT",
   long_description=long_description,
   author='Serif Dogru',
   author_email='dogruserif12@gmail.com',
   classifiers=classifiers,
   url="",
   packages=['mycalculator_SD'],  #same as name
   install_requires=[], #external packages as dependencies
   scripts=[]
)






