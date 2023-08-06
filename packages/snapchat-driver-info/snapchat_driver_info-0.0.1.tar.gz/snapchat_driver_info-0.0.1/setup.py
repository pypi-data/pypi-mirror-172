from setuptools import setup, find_packages


VERSION = "0.0.1"
DESCRIPTION = "A basic profile search bot for snapchat"
LONG_DESCRIPTION = "A basic driver bot for snapchat"

# Setting up
setup(
    name="snapchat_driver_info",
    version=VERSION,
    author="Abdessamad BAAHMED",
    author_email="baahmedabdessamad@outlook.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "async-generator",
        "attrs",
        "beautifulsoup4",
        "bs4",
        "certifi",
        "cffi",
        "cryptography",
        "h11",
        "idna",
        "outcome",
        "pycparser",
        "pyOpenSSL",
        "PySocks",
        "selenium",
        "sniffio",
        "sortedcontainers",
        "soupsieve",
        "trio",
        "trio-websocket",
        "urllib3",
        "wsproto",
    ],
    keywords=["python", "snapchat", "scrapping", "search"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
