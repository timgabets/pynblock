from setuptools import setup

setup(name='pynblock',
      version='0.23',
      
      description='Payment card industry crypto library - PIN blocks, card/PIN verification values calculation etc.',
      long_description=open('README.rst').read(),
      
      classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        
        'Topic :: Communications',
        'Intended Audience :: Developers',
      ],
      
      keywords='payment crypto card pin cvv csc pinblock',
      
      url='https://github.com/timgabets/pynblock',
      author='Tim Gabets',
      author_email='tim@gabets.ru',
      
      license='LGPLv2',
      packages=['pynblock'],
      install_requires=['pycrypto'],
      zip_safe=True)