from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='PyAdminDash',
   version='1.0',
   description='monitoring and administration system linux tool',
   license="MIT",
   long_description=long_description,
   author='Abdelmoumen Drici, Boudjemma Djawed',
   author_email='abdelmoumendrici@gmail.com, djawedbdj@gmail.com',
   packages=['project'],
   install_requires=['PyQt5', 'psutils','matplotlib','qtmodern','rxvt-unicode'],
)
