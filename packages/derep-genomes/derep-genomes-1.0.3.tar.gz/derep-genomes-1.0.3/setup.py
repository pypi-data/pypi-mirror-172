from setuptools import setup
import versioneer

requirements = [
    "pandas>=1.1.2",
    "scipy>=1.5.2",
    "networkx>=2.5",
    "simple-slurm>=0.2.2",
    "tqdm>=4.62.2",
    "PyYAML>=5.4",
    "leidenalg>=0.8.2",
    "python-igraph>=0.8.3",
    "biopython>=1.78",
]

setup(
    name="derep-genomes",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A simple genome de-replication tool with fastANI",
    license="GNUv3",
    author="Antonio Fernandez-Guerra",
    author_email="antonio@metagenomics.eu",
    url="https://github.com/genomewalker/derep-genomes",
    packages=["derep_genomes"],
    entry_points={"console_scripts": ["derepG=derep_genomes.__main__:main"]},
    install_requires=requirements,
    keywords="derep-genomes",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
