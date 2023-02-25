from setuptools import setup

with open("Readme.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="b35t",
    version="1.0.0",
    description="Tool to connect to B35T+.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastian",
    author_email="hackwiki2.0@gmail.com",
    license="MIT License",
    packages=['b35t'],
    package_dir={'b35t': 'b35t/'},
    install_requires=[
        'pexpect',
        'ptyprocess'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux"
    ],
    entry_points={
        'console_scripts': [
            'b35t = b35t.b35t:main'
        ]
    },
)
