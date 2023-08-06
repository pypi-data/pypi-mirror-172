import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitronit",
    version="1.0.1",
    author="Bitronit",
    description="Bitronit Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        'Source': 'https://github.com/Bitronit/Bitronit-Python/'
    },
    packages=['bitronit', 'bitronit.models'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license_files = ('LICENSE'),
    python_requires='>=3.7', 
    install_requires=['requests>=2.28.1', 'simplejson>=3.17.6', 'python-dateutil>=2.8.2'],
    keywords="bitronit exchange api sdk rest client"
)