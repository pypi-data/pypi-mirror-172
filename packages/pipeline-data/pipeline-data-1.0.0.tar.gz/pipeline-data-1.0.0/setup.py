# -*- coding:utf-8 -*-

# @Time      :2022/10/21 14:26
# @Author    :huangkewei

import setuptools

setuptools.setup(
    name='pipeline-data',
    version='1.0.0',
    author='zhongbiao',
    description='数据同步',
    packages=setuptools.find_packages(),
    install_requires=[
        'sqlalchemy==1.3.22',
        'pottery==3.0.0',
        'werkzeug==2.2.1',
        'regex==2022.7.25',
        'cchardet==2.1.7',
        'pymysql==0.9.3'
    ]
)

# print(setuptools.find_packages())


