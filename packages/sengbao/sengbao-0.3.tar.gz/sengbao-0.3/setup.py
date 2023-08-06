from setuptools import setup

setup(name='sengbao',
      version='0.3',
      description='High Performance Maximum Likelihood Estimations',
      url='http://github.com/ibab/python-mle',
      author='sengbao',
      license='MIT',
      packages=['mle', 'mle.distributions'],
      install_requires=[
          'numpy',
          'scipy',
          'theano',
          'iminuit'
      ],
      zip_safe=False)
