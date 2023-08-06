from setuptools import setup

setup(name='sengbao',
      version='0.2',
      description='High Performance Maximum Likelihood Estimations',
      url='http://github.com/ibab/python-mle',
    #   author='Igor Babuschkin',
    #   author_email='igor@babuschk.in',
      license='MIT',
      packages=['mle', 'mle.distributions'],
      install_requires=[
          'numpy',
          'scipy',
          'theano',
          'iminuit'
      ],
      zip_safe=False)
