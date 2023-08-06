import setuptools

setuptools.setup(name='sengbao',
      version='0.4',
      description='High Performance Maximum Likelihood Estimations',
      url='http://github.com/ibab/python-mle',
      author='sengbao',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'numpy',
          'scipy',
          'theano',
          'iminuit'
      ],
      zip_safe=False)
