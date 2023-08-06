from setuptools import *
# from distutils.core import setup

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

setup(
    name='demo4pypi',  # 包名称
    version='1.0.2',  # 版本
    author='Jason',  # 作者
    author_email='jason@rimeix.com',  # 作者邮箱
    description='This is for managing invoice',  # 描述
    long_description=readme(),  # 长文描述
    long_description_content_type='text/markdown',  # 长文描述的文本格式
    keywords='pypi',  # 关键词
    packages=find_packages(),
)
