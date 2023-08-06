from setuptools import setup, find_packages

setup(
    name='rajant_api',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "grpcio==1.56.2",
        "grpcio-tools==1.56.2",
        "protobuf==4.23.4"
    ],
    url='https://github.com/MrTwister96/rajant-api',
    license='License :: Free For Educational Use',
    author='Schalk Olivier',
    author_email='olivierschalk1@gmail.com',
    description='Library for communicating with Rajant Breadcrumb devices using the BCAPI implemented in Python3',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Free For Educational Use',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
