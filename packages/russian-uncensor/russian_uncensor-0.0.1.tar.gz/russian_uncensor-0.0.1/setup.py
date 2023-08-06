try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='russian_uncensor',
    packages=['russian_uncensor'],
    version='0.0.1',
    license='MIT',
    description='Uncensor for russian masked or separated obscene words based on frequent letters, bi- and tri-grams analysis',
    long_description='',
    author='Alex Klyuev',
    author_email='Klyukvanstalker@gmail.com',
    url='https://github.com/AlexKly/russian_uncensor',
    download_url='https://github.com/AlexKly/russian_uncensor/archive/refs/tags/0.0.1.tar.gz',
    keywords=['uncensor', 'obscene words', 'swear words', 'n-grams'],
    install_requires=['marisa_trie'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
