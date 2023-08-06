from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3.10',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Education',
    'Topic :: Software Development :: Bug Tracking',
]

setup(
  name='pavit_basic_calculator',
  version='0.0.1',
  description='Use for pratice create python library',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pavit Suwansiri',
  author_email='pavit.suwansiri@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['numpy', 'pandas']  # numpy 
)