from setuptools import setup

setup(
    name="librus_terminal",
    version="0.1.0",
    author="Piotr Ginał",
    packages=["librus_terminal"],
    install_requires=[
        "librus_scraper"
    ],
    entry_points={
        "console_scripts": [
            "librus_terminal=librus_terminal.__main__:main"
        ]
    }
)
