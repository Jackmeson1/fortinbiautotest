from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fnbi-automated-testing",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pytest~=8.3.2",
        "selenium~=4.24.0",
        "pywinauto==0.6.8",
        "psutil~=6.0.0",
        "PyYAML~=6.0.2",
        "open-clip-torch~=2.32.0",
        "faiss-cpu~=1.11.0",
        "numpy~=2.2.6",
        "torch~=2.7.1",
        "pillow~=11.2.1",
        "scikit-image~=0.25.2",
        "requests~=2.32.3",
        "pygetwindow~=0.0.9",
        "pywin32==310; platform_system=='Windows'",
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
