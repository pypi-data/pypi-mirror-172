# encoding: utf-8
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
long_description = None
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='lzm_comtools', # 包名称
      packages= find_packages(exclude=["lzm_comtools"]),
      version='1.0.0', # 版本
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python', 'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9'
      ],
      install_requires=['ping3'],
      entry_points={'console_scripts': ['lzmct=lzm_comtools.lzm_comtools_module:main']},
      package_data={'': ['*.json']},
      auth='lizhuming', # 作者
      author_email='821350342@qq.com', # 作者邮箱
      description='com tools', # 介绍
      long_description=long_description, # 长介绍，在pypi项目页显示
      long_description_content_type='text/markdown', # 长介绍使用的类型，我使用的是md
      url='', # 包主页，一般是github项目主页
      license='MIT', # 协议
      keywords='com tools lzm lzm_comtools') # 关键字 搜索用