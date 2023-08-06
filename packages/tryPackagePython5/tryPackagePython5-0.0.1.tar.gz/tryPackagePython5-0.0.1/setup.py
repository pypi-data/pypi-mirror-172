from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'tryPackagePython5',
    version='0.0.1',
    description='My own first package',
    long_description='this would be a long description',
    url='',
    author='Alex Pacheco',
    author_email='<alex.pacheco.reynado@gmail.com>',
    license='MIT',
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    install_requires=['numpy', 'numba']
)