from setuptools import setup, find_packages

setup(
    name="apt-emulation-platform",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Full-Spectrum Adversary Emulation Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apt-emulation-platform",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pyyaml>=6.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "apt-emulate=main:main",
        ],
    },
)
