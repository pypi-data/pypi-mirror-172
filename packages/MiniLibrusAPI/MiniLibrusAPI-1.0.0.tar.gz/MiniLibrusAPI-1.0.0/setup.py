from setuptools import setup, find_packages

classifiers = [
  'License :: OSI Approved :: MIT License',
  'Intended Audience :: Developers',
  'Operating System :: OS Independent',
  'Programming Language :: Python :: 3.5',
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  'Programming Language :: Python :: 3.9'
]

setup(
    name='MiniLibrusAPI',
    version='1.0.0',
    description='Łatwy do użycia moduł MiniLibrusAPI.',
    long_description=open('README.md', encoding="utf8").read(),
    long_description_content_type="text/markdown",
    url='',
    author='faktorr',
    author_email='patryktarasiuk04@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='MiniLibrusAPI',
    packages=find_packages(),
    install_requires=['requests_html']
)