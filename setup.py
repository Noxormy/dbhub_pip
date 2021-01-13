import setuptools

setuptools.setup(
    name="dbhub",  # Replace with your own username
    version="0.5.1",
    author="Noxormy",
    author_email="noxormy@gmail.com",
    description="Package to create db in one-click",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/Noxormy/dbhub_pip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.2.0',
        'easydict>=1.9.0'
    ]
)
