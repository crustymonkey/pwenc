    
from distutils.core import setup
import os

cur_dir = os.path.dirname(__file__)
req_file = os.path.join(cur_dir, 'requirements.txt')
requirements = [l.strip() for l in open(req_file).readlines() if l.strip()]

setup(name='pwenc',
    version='0.2.0',
    author='Jay Deiman' ,
    author_email='admin@splitstreams.com' ,
    url='http://splitstreams.com' ,
    license='GPLv2' ,
    platforms=['unix'] ,
    install_requires=requirements,
    description='Password file encrypter and decrypter' ,
    scripts=['pwenc.py']
)
