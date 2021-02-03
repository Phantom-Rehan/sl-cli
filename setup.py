import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sl-cli-astroanax",
    version="0.0.1",
    author="Rehan Tadpatri",
    author_email="astroanax@outlook.com",
    description="CLI application for SimpleLogin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astroanax/simplelogin-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "sl_cli = sl_cli.__main__:main",
        ],
    },
    install_requires=["requests", "xdg"],
)
