from setuptools import find_packages, setup

setup(
    name="PSI",
    author="Osama Abbas",
    author_email="oabbas2512@gmail.com",
    maintainer="Osama Abbas",
    maintainer_email="oabbas2512@gmail.com",
    url="https://github.com/Tes3awy/PSIRT",
    keywords=["Cisco", "PSIRT", "OpenVuln", "API", "Flask"],
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    license="LICENSE",
    install_requires=[
        "wheel",
        "Flask",
        "Flask-WTF",
        "Flask-Compress",
        "Flask-HTMLmin",
        "requests",
        "requests-oauthlib",
        "python-dotenv",
    ],
)
