import os.path

from setuptools import setup, find_packages

HERE = os.path.dirname(os.path.abspath(__file__))


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    author="Michael Green",
    author_email="1mikegrn@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="a Linux window manager based on Microsoft's FancyZones",
    entry_points={"console_scripts": ["snappy=snappyzones.__main__:main"]},
    include_package_data=True,
    install_requires=["python3-xlib>=0.15"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="snappyzones",
    packages=find_packages(where="src"),
    package_data={"": ["*.json", "*.txt"]},
    package_dir={"": "src"},
    python_requires=">=3.8",
    tests_require=["pytest"],
    url="https://github.com/1mikegrn/snappyzones",
    version="0.0.8",
)
