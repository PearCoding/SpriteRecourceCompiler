# encoding: utf-8

from distutils.core import setup

setup(
    name='SpriteResourceCompiler',
    version='1.0',
    packages=['src'],
    url='http://pearcoding.eu',
    license='https://opensource.org/licenses/MIT',
    author='Ömercan Yazici',
    author_email='omercan@pearcoding.eu',
    description='A basic sprite resource processing and packing compiler.',
    classifiers=[
                      'License :: OSI Approved :: MIT License',
                      'Programming Language :: Python :: 3.3',
                      'Programming Language :: Python :: 3.4',
                      'Programming Language :: Python :: 3.5',
                      'Programming Language :: Python :: Implementation :: PyPy3',
                  ],
    requires=['Pillow']
)
