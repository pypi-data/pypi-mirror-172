import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ecmind_spring_config',
    version='0.0.9',
    author='Ulrich Wohlfeil',
    author_email='info@ecmind.ch',
    description='Helper module for spring alike configuration loading plus spring cloud config client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.ecmind.ch/open/ecmind_spring_config',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'PyYAML>=5.4.1', 
        'deepmerge>=0.3.0',
        'toml>=0.10.2'
    ],
    extras_require = { }
)