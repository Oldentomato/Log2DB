import setuptools

setuptools.setup(
    name="log2db",
    version="0.0.3",
    license='MIT',
    author="WooSung Jo",
    author_email="jwsjws99@gmail.com",
    description="Send Deep Learning Training,Test Log To DB",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Oldentomato/Log2DB",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)