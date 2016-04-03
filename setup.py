from setuptools import setup, find_packages

version = '0.0.1.dev0'

setup(
    name='blackpearl',
    version=version,
    long_description=open("README.rst").read(),
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'twisted',
        'pyserial',
    ],
)
