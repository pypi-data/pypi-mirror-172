from setuptools import setup, find_packages

setup(name='moreprot',
      version="1.0.2",
      url='https://github.com/mhlee216/MoReProt',
      packages=find_packages(),
      author='Myeonghun Lee',
      author_email="leemh216@gmail.com",
      description='MoReProt: Molecular Fingerprint Recombination-based Protein Fingerprint.',
      long_description='MoReProt: Molecular Fingerprint Recombination-based Protein Fingerprint.',
      install_requires=["numpy >= 1.19.0", "rdkit >= 2021.09.2"],
      classifiers=['License :: OSI Approved :: MIT License'])
