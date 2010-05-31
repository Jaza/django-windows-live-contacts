from setuptools import setup, find_packages
 
setup(name='django-windows-live-contacts',
    version='0.1',
    description='Retrieve the contacts from the Windows Live (Hotmail) account of a user of your Django site',
    long_description=open('README.txt').read(),
    author='Jeremy Epstein',
    author_email='je@digitaleskimo.net',
    url='http://github.com/Jaza/django-windows-live-contacts',
    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ]
)
