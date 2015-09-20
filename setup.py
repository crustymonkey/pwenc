    
from distutils.core import setup

setup(name='pwenc',
    version='0.2.0',
    author='Jay Deiman' ,
    author_email='admin@splitstreams.com' ,
    url='http://splitstreams.com' ,
    license='GPLv2' ,
    platforms=['unix'] ,
    install_requires=['pycrypto>=2.0', 'six>=1.9.0']
    description='Password file encrypter and decrypter' ,
    scripts=['pwenc.py']
)
