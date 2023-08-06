#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "BriefEvaluation", #项目名称
    version = "0.0.1", #版本号
    keywords = ["pip", "BriefEvaluation"], #关键词
    description = "This is a package for doing a comprehensive evaluation",#简介
    long_description = "This is a package for doing a comprehensive evaluation",#长简介
    license = "MIT Licence",#开源许可

    url = "https://gitee.com/zkspongebob/evaluation",#项目地址
    author = "zkSponegBob",#项目作者
    author_email = "zkSpongeBob@126.com",#作者邮箱

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy", "pandas"]
)