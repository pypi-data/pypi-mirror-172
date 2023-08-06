from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "stone91_tools",      #这里是pip项目发布的名称
    version = "0.0.1",  #版本号，数值大的会优先被pip
    keywords = ["pip", "stone91_tools"],			# 关键字
    description = "stone91's private tools.",	# 描述
    long_description = "includes plotting ml imageprocessing etc.",
    license = "MIT Licence",		# 许可证

    url = "https://github.com/370025263/stone91_tools",     #项目相关文件地址，一般是github项目地址即可
    author = "stone91",			# 作者
    author_email = "mengshi2022@ia.ac.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy", "matplotlib", "IPython"]          #这个项目依赖的第三方库
)
