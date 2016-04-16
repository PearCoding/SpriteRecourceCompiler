# encoding: utf-8

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

kwargs = {}

with open('README.md') as f:
    kwargs['long_description'] = f.read()

if setuptools is not None:
    install_requires = ['pillow']
    kwargs['install_requires'] = install_requires

setup(
    name='SpriteResourceCompiler',
    version='1.0',
    packages=['src'],
    package_data={
        "src.tests": [
            "test.png"
            ],
        },
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
    **kwargs
)
