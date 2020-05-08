from setuptools import setup

with open("README.rst", 'r') as f:
    long_description = f.read()

setup(
   name='GUI-admin-tool',
   version='1.0',
   description='monitoring and administration system linux tool',
   license="MIT",
   long_description=long_description,
   author='Abdelmoumen Drici, Boudjemma Djawed',
   author_email='abdelmoumendrici@gmail.com, djawedbdj@gmail.com',
   packages=['project'],  #same as name
   install_requires=['PyQt5', 'psutil','matplotlib','qtmodern'], #external packages as dependencies
)
