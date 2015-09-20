    
from distutils.core import setup
import os

cur_dir = os.path.dirname(__file__)
req_file = os.path.join(cur_dir, 'requirements.txt')
requirements = [l.strip() for l in open(req_file).readlines() if l.strip()]

setup(name='pwenc',
    version='0.2.0',
    author='Jay Deiman' ,
    author_email='admin@splitstreams.com' ,
    url='http://stuffivelearned.org' ,
    license='GPLv2' ,
    platforms=['unix'] ,
    description='This is a simple encrypted file manager for use with a '
        'passphrase',
    long_description='This is a simple cli that will allow to '
        'encrypt/decrypt files given a passphrase.  This is meant to be '
        'simple/easy to use.  It uses sha512 for hashing and AES 256 for '
        'the symmetric encryption.',
    install_requires=requirements,
    description='Password file encrypter and decrypter' ,
    scripts=['pwenc.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
    ],

)
