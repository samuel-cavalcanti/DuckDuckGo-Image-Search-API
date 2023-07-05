"""setup."""
import setuptools
from pathlib import Path

setuptools.setup(
    name="duckduckgo_images_api",
    version="0.0.2",
    url="https://github.com/samuel-cavalcanti/DuckDuckGo-Image-Search-API.git",
    author="Deepan Prabhu Babu and Samuel Cavalcanti",
    description="Download DuckDuckGo Image Search Resuts - Scraped using Python 3.11",
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    keywords="duckduckgo image api",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=Path('requirements.txt').read_text().splitlines(),
    extras_require={
        'packaging': ['setuptools>=42'],
    },
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
)
