from setuptools import setup, find_packages
required = [
    'numpy',
    'scipy',
	'pandas',
	'matplotlib',
	'scikitlearn',
]
setup(
    name = "Autolivlib",
    version = "3.1.1",
    packages = find_packages(),
    author="Yujin Wang",
    author_email="Chaos1984@163.com",
	package_data={'':['*.txt','*.pptx','*.tcl','*.mvw','*.png','*.jpg','*.jpeg','*.ppt','*.bat']},
    include_package_data = True,	
	license = 'LICENSE'
)