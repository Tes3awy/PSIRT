from setuptools import find_packages, setup

setup(
    name="PSI",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "wheel",
        "Flask",
        "Flask-WTF",
        "Flask-Limiter[mongodb]",
        "Flask-Compress",
        "Flask-HTMLmin",
        "requests",
        "requests-oauthlib",
        "python-dotenv",
    ],
)
