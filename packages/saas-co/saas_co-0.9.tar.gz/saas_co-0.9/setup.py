from setuptools import setup, find_packages

setup(
    name='saas_co',
    version='0.9',
    license='MIT',
    author="David Schwartz",
    author_email='david.schwartz@devfactory.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='cost optimization cur',
    install_requires=[
          'boto3',
          'botocore',
          'pandas',
          'awswrangler'
      ],
)
