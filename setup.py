from setuptools import setup

setup(
    name='notion-gcal-sync',
    version='1.0.0',
    packages=['events', 'clients', 'unit'],
    package_dir={'': 'notion-gcal-sync'},
    url='https://github.com/Ravio1i/notion-gcal-sync',
    license='GNU General Public License v3.0',
    author='Luka',
    author_email='luka.kroeger@gmail.com',
    description='Bidirectional synchronize calendar events within notion and google calendar '
)
