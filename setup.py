from setuptools import setup
import os


if os.path.isfile('requirements.txt'):
    with open('requirements.txt', 'r') as requirements_file:
        install_requires = requirements_file.read().splitlines()


setup(
    name='tdf_batch_chromatogram_mobilogram_export',
    version='0.1.0',
    url='https://github.com/gtluubruker/tdf_batch_chromatogram_mobilogram_export',
    license='Apache License 2.0',
    author='Gordon T. Luu',
    author_email='gordon.luu@bruker.com',
    packages=['tdf_batch_chromatogram_mobilogram_export'],
    description='Batch export chromatograms and mobilograms from Bruker timsTOF *.d TDF data.',
    entry_points={'console_scripts': ['export_chromatogram=tdf_batch_chromatogram_mobilogram_export.util:export_chromatogram',
                                      'export_mobilogram=tdf_batch_chromatogram_mobilogram_export.util:export_mobilogram']},
    install_requires=install_requires,
    setup_requires=install_requires
)
