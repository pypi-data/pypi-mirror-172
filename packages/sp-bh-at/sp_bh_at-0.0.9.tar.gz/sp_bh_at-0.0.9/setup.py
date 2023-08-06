from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

requirements = []
for line in open('requirements.txt'):
    li = line.strip()
    if not li.startswith('#'):
        requirements.append(line.rstrip())


VERSION = (0, 0, 9)
__version__ = '.'.join(map(str, VERSION))


setup(
    name='sp_bh_at',
    version=__version__,
    author='Michel Metran',
    author_email='michelmetran@gmail.com',
    description='Dados Espaciais do Comitê de Bacias do Alto Tietê ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/open-geodata/sp_bh_at',
    keywords='python, dados espaciais, geoprocessamento',

    # Python and Packages
    python_requires='>=3',
    install_requires=requirements,

    # Entry
    # Our packages live under src but src is not a package itself
    #package_dir={'': 'src'},

    # Quando são diversos módulos...
    #packages=find_packages('src', exclude=['test']),
    packages=find_packages(),

    # Dados
    include_package_data=True,
    package_data={'sp_bh_at': ['data/output/geo/*.7z']},

    # Classificação
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese',
        'Intended Audience :: Developers',
    ],
)
