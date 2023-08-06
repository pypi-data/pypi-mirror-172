# -*- encoding: utf-8 -*-
"""
@File: setup.py
@Time: 2022/10/20 9:52
@Author: HSQF
@Software: PyCharm

"""
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pdftoxlsx_v1",  # 模块名称
    version="1.0.1",  # 当前版本
    author="hsqf",  # 作者
    author_email="haishangqingfeng@foxmail.com",  # 作者邮箱
    description="一个非常用于将pdf转换为xlsx的包",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="https://github.com/wupeiqi/fucker",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'requests',
    ],
    python_requires='>=3',
)