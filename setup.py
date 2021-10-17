from setuptools import setup, find_packages

setup(
    name='notion-gcal-sync',
    version='1.0.0',

    url='https://github.com/Ravio1i/notion-gcal-sync',
    license='GNU General Public License v3.0',
    author='Luka',
    author_email='luka.kroeger@gmail.com',
    description='Bidirectional synchronize calendar events within notion and google calendar',
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['notion-gcal-sync=notion_gcal_sync.__main__:main']
    },
    packages=find_packages(include=['notion_gcal_sync', 'notion_gcal_sync.*']),
    package_data={'notion_gcal_sync': ['config.example.yml']},
    include_package_data=True,
    install_requires=[
        'notion-client==0.7.0',
        'google-api-python-client==2.23.0',
        'google-auth-oauthlib==0.4.6',
        'pyyaml==5.4.1',
        'pandas==1.3.3'
    ],
    setup_requires=['pytest-runner'],
    test_requires=[
        'pytest~=6.2.4',
        'pytest-cov==3.0.0',
        'flake8==4.0.1'
    ]
)
