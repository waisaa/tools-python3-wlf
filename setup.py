from setuptools import setup, find_packages

VNU = 8
VERSION = f'0.0.{VNU}'
README = ''
with open("README.md", "r", encoding="utf-8") as fh:
    README = fh.read()

setup(name="pywlf",
      version=VERSION,
      keywords=["wlflog", "wlffile", "wlfdate", "wlfssh", "wlfcore", "wlfinfluxdb", "wlfmysql", "wlfredis", "wlfminio", "wlfkafka", "wlfhttp"],
      description="Common utils for python3.",
      long_description=README,
      long_description_content_type="text/markdown",
      license="MIT Licence",
      url="https://github.com/waisaa/tools-python3-wlf",
      author="waisaa",
      author_email="waisaa@qq.com",
      packages=find_packages(),
      include_package_data=True,
      platforms="any",
      python_requires='>=3.7',
      install_requires=['colorlog', 'openpyxl', 'chardet'])
