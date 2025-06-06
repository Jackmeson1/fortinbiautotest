from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fnbi-automated-testing",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pytest",
        "selenium",
        "pywinauto",
        "psutil",
        "PyYAML",
        "open-clip-torch",
        "faiss-cpu",
    ],
    entry_points={
        "console_scripts": [
            "run-fnbi-tests=scripts.run_tests:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated testing suite for FortiNBI application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fnbi-automated-testing",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
