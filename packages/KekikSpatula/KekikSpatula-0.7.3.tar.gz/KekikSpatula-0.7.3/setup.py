# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from setuptools import setup
from io         import open

setup(
    author       = "keyiflerolsun",
    author_email = "keyiflerolsun@gmail.com",

    packages     = ["KekikSpatula"],

    name         = "KekikSpatula",
    version      = "0.7.3",
    url          = "https://github.com/keyiflerolsun/KekikSpatula",
    description  = "Siz uğraşmayın diye biz uğraştık.. ~ dızz 🐍",
    keywords     = ["KekikSpatula", "KekikAkademi", "keyiflerolsun"],

    long_description_content_type   = "text/markdown",
    long_description                = "".join(open("README.md", encoding="utf-8").readlines()),
    include_package_data            = True,

    license     = 'GPLv3+',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3'
    ],

    python_requires     = '>=3.10',
    install_requires    = [
        "setuptools",
        "wheel",
        "requests",
        "regex",
        "Kekik",
        "pyTrendyol",
        "cloudscraper",
        "tabulate",
        "beautifulsoup4",
        "lxml",
        "html5lib",
        "pandas",
        "pytube",
        "pytz",
        "parsel",
        "pyshorteners",
        "requests-html"
    ]
)
