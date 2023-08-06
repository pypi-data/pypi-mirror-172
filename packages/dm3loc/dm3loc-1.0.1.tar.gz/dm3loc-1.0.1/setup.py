from setuptools import setup, find_packages

setup(
    name='dm3loc',
    version='1.0.1',
    description='Deep-learning Framework with Multi-head Self-attention for Multi-label mRNA Subcellular Localization Prediction and Analyses',
    author='Duolin Wang',
    author_email='deepduoduo@gmail.com',
    install_requires = ['numpy', 'scipy', 'scikit-learn', 'pillow', 'h5py', 'keras>=2.2.4', 'tensorflow>=1.13.1'],
    packages=find_packages(),
    include_package_data=True,
    package_data = {
        'model': ['DM3Loc/model/*'],
        'testdata': ['DM3Loc/testdata/*']
    }

)
