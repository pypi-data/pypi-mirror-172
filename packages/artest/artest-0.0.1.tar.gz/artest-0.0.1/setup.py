#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name = "artest",      # 这里是pip项目发布的名称
    version = "0.0.1",    # 版本号，数值大的会优先被pip
    keywords = ("pip", "test"),
    description = "A test algorithm framework",
    long_description = "A test algorithm framework",
    # long_description_content_type="text/markdown",
    license = "MIT Licence",

    url = "",     #项目相关文件地址，一般是github
    author = "ripplepiam",
    author_email = "example@mail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [""],          #这个项目需要的第三方库
    # extra params
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)