from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappyflaskimpex",
      version="1.0.0",
      description="Flask Endpoints for Database Import and Export",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-flask-impex",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappyflaskimpex"
      ],
      install_requires=[
            "flask",
            "pbu",
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
