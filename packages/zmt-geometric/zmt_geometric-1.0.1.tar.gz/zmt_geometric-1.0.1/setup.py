from setuptools import setup, find_packages

setup(name='zmt_geometric',
      version="1.0.1",
      description='Geometric series interfaces.',
      license='MIT',
      author='Michael Zhang',
      author_email='zmtgoodboy2@gmail.com',
      packages=find_packages(),
      platforms = "any",
      install_requires=[
          'uvicorn>=0.18.3',
          'fastapi>=0.85.1',
          'pydantic>=1.10.2'
      ],
      zip_safe=False)
