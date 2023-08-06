from setuptools import *
# from distutils.core import setup

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

setup(
    name='zxinvoice',  # 包名称
    version='1.0',  # 版本
    author='Jason',  # 作者
    author_email='jason@rimeix.com',  # 作者邮箱
    description='This is for managing invoice',  # 描述
    long_description=readme(),  # 长文描述
    long_description_content_type='text/markdown',  # 长文描述的文本格式
    keywords='zxinvoice,invoice,pyinvoice',  # 关键词
    # url='',  # 项目主页
    classifiers=[],
    # license='Apache License 2.0',  # 许可证
    packages=find_packages(),
    install_requires=[
        'chinesecalendar',
        'baidu-aip',
        'chardet',
        'pywebio',
        'pysqlcipher3',
    ],
    python_requires='>=3.6',
    # entry_points={
    #     'console_scripts': [
    #         'zxinvoice = zxinvoice.main:main' # 格式为'命令名 = 模块名:函数名'
    #     ]
    # }
)
