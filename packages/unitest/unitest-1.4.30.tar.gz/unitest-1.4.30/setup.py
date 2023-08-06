import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('README.md', "r", encoding="utf-8") as version:
    version_number = version.readlines()[-1].split(":")[-1]

setuptools.setup(
    name="unitest",
    version=version_number,
    author="Zeta",
    description="Utilities required for performance and functional tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/zetaengg/unitest_plutus/src/main/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "selenium>=4.1.1",
        "gevent>=21.12.0",
        "geventhttpclient>=1.5.5",
        "psycogreen>=1.0.2",
        "locust==2.12.1",
        "requests>=2.28.1",
        "jsonpath-ng>=1.5.3",
        "greenlet==1.1.2",
        "psycopg2-binary>=2.9.3",
        "assertpy>=1.1",
        "pytest>=7.1.1",
        "allure-pytest>=2.9.45",
        "pytest-json-report>=1.5.0",
        "webdriver-manager>=3.8.2",
        "faker>=13.15.0",
        "exrex>=0.10.5",
        "decorator>=5.1.1",
        "influxdb_client>=1.31.0",
        "prometheus_client>=0.14.0",
        "curlify>=2.2.1",
        "PyJWT>=2.4.0",
        "pytest-xdist>=2.5.0",
        "pytest-rerunfailures>=10.2",
        "fast_map>=0.0.7",
        "pytest-order>=1.0.1",
        "gunicorn>=20.1.0",
        "fastapi-utils>=0.2.1",
        "uvicorn>=0.18.2",
        "lxml>=4.9.1",
        "beautifulsoup4>=4.11.1",
        "cryptography>=38.0.1",
        "pandas==1.5.0",
        "python-dotenv>=0.21.0",
        "PyByteBuffer>=1.0.5"
    ]
)
