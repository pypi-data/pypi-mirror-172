import setuptools 
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="onsite", 
    version="0.1.9",   
    author="Yan Huang",   
    author_email="huangyan520@tongji.edu.cn",   
    description="A tool package for Onsite",
    long_description=long_description,    
    long_description_content_type="text/markdown",
    url="https://gitee.com/huangyansmile/onsite-develop", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        'numpy',
        'shapely',
        'pandas',
        'matplotlib'
    ],
    python_requires='>=3.6',    #对python的最低版本要求
)