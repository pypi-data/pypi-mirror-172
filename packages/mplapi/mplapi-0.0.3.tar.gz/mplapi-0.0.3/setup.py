import setuptools

setuptools.setup(
    name='mplapi',
    version='0.0.3',
    author='Nana-Miko',
    author_email='1121917292@qq.com',
    description='提供MPL(Mirai Python Loader)插件开发API',
    url='https://nana-miko.github.io/Mirai-Python-Loader-Docs/',
    packages=setuptools.find_packages(exclude=["Pipfile", ".idea"]),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],

)
