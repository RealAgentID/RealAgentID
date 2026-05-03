from setuptools import setup, find_packages

setup(
    name="realagentid",
    version="0.1.0",
    description="Cryptographic identity verification for AI agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="RealAgentID",
    url="https://github.com/RealAgentID/RealAgentID",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "redis",
    ],
    python_requires=">=3.12",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
