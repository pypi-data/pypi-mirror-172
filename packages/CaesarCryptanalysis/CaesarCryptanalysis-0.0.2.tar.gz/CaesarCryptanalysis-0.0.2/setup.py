import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CaesarCryptanalysis",
    version="0.0.2",
    author="izuru inose",
    author_email="i.inose0304@gmail.com",
    description="It is a tool to decipher Caesar ciphers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/i-inose/Caesar-Cryptanalysis-App",
    project_urls={
        "Bug Tracker": "https://github.com/i-inose/Caesar-Cryptanalysis-App",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['CaesarCryptanalysis'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'CaesarCryptanalysis = CaesarCryptanalysis:main'
        ]
    },
)
