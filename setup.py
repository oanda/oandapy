from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='oandapy',
      version=version,
      description="Python wrapper for the OANDA REST API",
      long_description="""\
""",
      classifiers=[
            'Programming Language :: Python',
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry'
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='OANDA FOREX wrapper REST API',
      author='OANDA',
      author_email='api@oanda.com',
      url='http://developer.oanda.com/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      test_suite="tests",
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
