from setuptools import setup, find_packages

setup(
    name='toolbox',
    version='1.0.0',
    packages=['toolbox', 'toolbox.default_module'],
    entry_points={
        'console_scripts': [
            'toolbox = toolbox.cli:main',
        ],
    },
    install_requires=[
    ],
    include_package_data=True,
)
    