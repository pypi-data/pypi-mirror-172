from setuptools import setup

setup (
    name='tools_hjh',
    version='1.2.15',
    author='HuaJunhao',
    author_email='huajunhao6@yeah.net',
    install_requires=[
          'dbutils'
        , 'PIL'
        , 'pymysql'
        , 'cx_Oracle'
        , 'paramiko'
        # , 'zipfile36'
        # , 'crypto'
        , 'requests'
    ],
    packages=['tools_hjh']
)
