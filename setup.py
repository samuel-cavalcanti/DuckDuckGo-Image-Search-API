"""setup."""
import setuptools

setuptools.setup(
    name="duckduckgo_images_api",
    version="0.0.1",
    url="https://github.com/samuel-cavalcanti/DuckDuckGo-Image-Search-API.git",
    author="Deepan Prabhu Babu and Samuel Cavalcanti",
    description="Download DuckDuckGo Image Search Resuts - Scraped using Python 3.7.5",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="duckduckgo image api",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['requests>=2.22.0', ],
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', 'flake8>=3.3.0', 'tox>=2.7.0', 'vcrpy>=1.11.1'],
    extras_require={
        'packaging': ['setuptools>=42'],
    },
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Programming Language :: Python :: 3.7.5',
        'License :: OSI Approved :: MIT License',
    ],
)
