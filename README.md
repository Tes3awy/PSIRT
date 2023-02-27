[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Tes3awy/PSIRT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Wheel: yes](https://img.shields.io/pypi/wheel/yes)

# Cisco PSIRT OpenVuln API Web App

![GIF](assets/psirt.gif)

Cisco PSIRT application takes advantage of the Cisco PSIRT OpenVuln RESTful API to search for CVEs and show all its data and related information from other sites not only to easily identify the CVE and its workarounds (if provided) but also to get all possible solutions at one place and to be up to date with any security vulnerability.

**This web app is your Google's search engine but for Cisco CVEs.**

## Table of Contents

1. [Features](#features)
2. [Solution Components](#solution-components)
3. [Usage](#usage)
4. [Installation](#installation)
5. [Dockerize](#dockerize)
6. [Screenshots](#screenshots)
7. [Documentation](#documentation)
8. [Disclaimer](#disclaimer)
9. [Use Case](#use-case)

## Features

- Using a set of search forms, you can get all information of a CVE by its ID, or even get all CVEs of not only IOS and IOS-XE, both NX-OS and NX-OS in ACI mode, but also ASA, FTD, FMC, and FXOS. You can also search for security advisories for a specific Cisco Product _(Partially supported)_ ([See why](https://community.cisco.com/t5/services-discussions/psirt-openvuln-api-pagination-issue/m-p/4760270#M938)).

- Fully Responsive on mobile devices.

## Solution Components

### Backend Components

1. [Python 3.9, 3.10, 3.11](https://www.python.org/downloads/)
2. [Flask](https://flask.palletsprojects.com/en/2.2.x/)
3. [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/) (For forms and server-side validation)
4. [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/) (For Rate-Limiting)
5. [MongoDB](https://www.mongodb.com/try/download/community) (For storing the Rate Limit in production deployment. `Disabled in development`)
6. [Requests](https://requests.readthedocs.io/en/latest/) (To send HTTP requests for API endpoints)
7. [Requests-OAuthlib](https://requests.readthedocs.io/en/latest/community/recommended/#requests-oauthlib) (To do OAuth authentication with Cisco API Console Backend Application)

### Frontend Components

1. [Cisco UI Kit](https://www.cisco.com/web/fw/cisco-ui/2.0.5/dist/css/cui-standard.min.css)
2. [jQuery 3.6.3](https://jquery.com/download/)
3. [ScrollReveal.js](https://scrollrevealjs.org/)
4. [Select2.js](https://select2.org/)

## Usage

Tested on:

1. Windows 10/11
2. Ubuntu Jammy 22.0.1

## Installation

1. Download or clone this repository.

```bash
$ git clone https://github.com/Tes3awy/PSIRT.git
$ cd PSIRT
```

2. Create a virtual environment and install requirements.

```bash
$ python3 -m venv .venv --upgrade-deps
$ source .venv/bin/activate
$ python3 -m pip install wheel
$ python3 -m pip install -r requirement.txt
```

3. Create a `config.py` next to `wsgi.py`.

```bash
$ cd PSIRT
$ touch config.py
```

4. Open `config.py` and paste the following snippet.

> To register a Cisco PSIRT OpenVuln API application on Cisco API Console (for `CLIENT_ID` and `CLIENT_SECRET`), follow a long with this [Cisco Guide](https://developer.cisco.com/docs/support-apis/#!application-registration/exploring-the-api-developer-portal) or this [Cisco Community Guide](https://community.cisco.com/t5/services-knowledge-base/accessing-the-cisco-psirt-openvuln-api-using-curl/ta-p/3652897) by Omar Santos.

```python
class Config(object):
    BASE_URL = "https://api.cisco.com/security/advisories/v2"  # New URL
    CLIENT_ID = "<YOUR_CISCO_CLIENT_ID>"  # From https://apiconsole.cisco.com/apps/myapps
    CLIENT_SECRET = "<YOUR_CISCO_CLIENT_SECRET>"  # From https://apiconsole.cisco.com/apps/myapps
    # You can run: python -c 'import secrets; print(secrets.token_hex())' twice to get two secret keys for the following secret keys.
    SECRET_KEY = "<A_SECRET_KEY>"
    WTF_CSRF_SECRET_KEY = "<A_SECRET_KEY_FOR_WTF_FORMS>"
    APP_ENV = "development"
    DEBUG = True
    TESTING = False
    RATELIMIT_STORAGE_URI = "memory://"


class ProductionConfig(Config):
    APP_ENV = "production"
    DEBUG = False
    RATELIMIT_STORAGE_URI = "redis://localhost:6379" # Change to MongoDB or Memcached depending on your choice
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_KEY_PREFIX = "PSI"
    RATELIMIT_IN_MEMORY_FALLBACK_ENABLED = True
```

5. Open terminal and run:

```bash
$ cd PSIRT
$ flask run
```

You should get the development webserver up and running:

```
$ flask run

* Serving Flask app 'run.py'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://xxx.xxx.x.x:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx

```

6. Open `localhost:8080` in your browser and you are ready to use the application.

7. If deployed in production, change the following line in `psiapp/__init__.py`

```python
...

def create_app(config_class=ProductionConfig):  # this line
    app = Flask(__name__)
    ...
```

## Dockerize

You can build and run the application in a Docker container

1. Replace `Config` with `ProductionConfig` at line 19 in `psiapp/__init__.py`

```bash
$ cd PSIRT
$ docker build --progress=plain --no-cache -t psirtimage:latest .
$ docker run -d -p 5000:5000 --name psi psirtimage
```

2. Open `localhost:5000` _(port 5000 this time)_ in your browser and you are ready to use your dockerized application.

## Screenshots

![Home](assets/home.jpg)
![CVE ID](assets/cve.jpg)
![Bug ID](assets/bug.jpg)
![OS-Version](assets/os-version.jpg)
![IOSXE](assets/iosxe.jpeg)
![Cisco Products](assets/product.jpg)

## Documentation

1. [Cisco PSIRT OpenVuln API Documentation](https://developer.cisco.com/docs/psirt/)
2. [API Reference](https://developer.cisco.com/docs/psirt/#!api-reference)
3. [PSIRT Knowledge Base](https://devnetsupport.cisco.com/hc/en-us/sections/115002851487-openVuln-API)
4. [Application Registration](https://developer.cisco.com/docs/support-apis/#!application-registration/application-registration)
5. [Accessing the Cisco PSIRT openVuln API Using curl](https://community.cisco.com/t5/services-knowledge-base/accessing-the-cisco-psirt-openvuln-api-using-curl/ta-p/3652897)

## Use Case

- You are working in an entity where you have to patch vulnerabilites in your Cisco Catalyst/Nexus switches or FTD. You can use `os - version` search form.
- You get an email from InfoSec to check some CVEs. You search on Google, but you get a bunch of irrelevant results and you don't know which one to open. This application narrows down the results to what exactly is needed with all links related to Cisco.

## Disclaimer

Code provided as-is. No warranty implied or included. Use the code for production at your own risk.
