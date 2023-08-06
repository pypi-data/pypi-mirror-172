from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyhard',
    version='2.1.1',
    description='Analyze, explore and visualize instance hardness within datasets',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['pyhard', 'pyhard.thirdparty'],
    url='https://gitlab.com/ita-ml/pyhard',
    download_url='https://gitlab.com/ita-ml/pyhard/-/archive/v2.1.1/pyhard-v2.1.1.tar.gz',
    license='MIT',
    author='Pedro Paiva',
    author_email='paiva@ita.br',
    install_requires=[
        'pandas>=1.3.0',
        'scikit-learn>=1.0.1',
        'numpy>=1.18.4',
        'PyYAML>=5.3',
        'scipy>=1.4.1',
        'panel>=0.13.1',
        'bokeh>=2.4.3',
        'holoviews>=1.15.0',
        'matplotlib>=3.2.2',
        'plotly>=5.9.0',
        'plotting>=0.0.7',
        'shapely>=1.7.0',
        'hyperopt>=0.2.4',
        'pyispace>=0.3.4',
        'deprecation>=2.1.0',
        'joblib>=1.0.0',
        'ncafs>=0.2',
        'typer>=0.4.1',
        'packaging>=21.0',
        'requests>=2.27.0'
    ],
    extras_require={
        'tests': [
            'pytest>=6.2'
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research"
    ],
    python_requires='>=3.8',
    package_data={'pyhard': ['data/**/*.csv', 'conf/config.yaml', 'midia/*']},
    entry_points={'console_scripts': ['pyhard=pyhard.cli:cli']}
)
