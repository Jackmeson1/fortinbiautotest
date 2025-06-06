from setuptools import setup, find_packages

setup(
    name="fnbi-automated-testing",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "selenium",
        "pywinauto",
        "psutil",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "run-fnbi-tests=scripts.run_tests:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated testing suite for FortiNBI application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fnbi-automated-testing",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
