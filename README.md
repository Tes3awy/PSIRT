[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![Wheel: yes](https://img.shields.io/pypi/wheel/yes)

# Cisco PSIRT OpenVuln API Web App

Cisco PSIRT application takes advantage of the Cisco PSIRT OpenVuln RESTful API to search for CVEs and show all its data and related information from other sites not only to easily identify the CVE and its workarounds (if provided) but also to get all possible solutions at one place and to be up to date with any security vulnerability.

**This web app is your Google's search engine but for Cisco CVEs.**

## Features

- Using a set of search forms, you can get all information of a CVE by its ID, or even get all CVEs of not only IOS and IOS-XE, both NX-OS and NX-OS in ACI mode, but also ASA, FTD, FMC, and FXOS. You can also search for security advisories for a specific Cisco Product _(Partially supported)_ ([See why](https://community.cisco.com/t5/services-discussions/psirt-openvuln-api-pagination-issue/m-p/4760270#M938)).

- Fully Responsive on mobile devices.

## Solution Components

### Backend Components

1. [Python 3.9, 3.10, 3.11](https://www.python.org/downloads/)
2. [Flask](https://flask.palletsprojects.com/en/2.2.x/)
3. [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/) (For forms and server-side validation)
4. [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/) (For Rate-Limiting)
5. [MongoDB](https://www.mongodb.com/try/download/community) (for storing the Rate Limit in production deployment. `Disabled for development`)
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

3. create a `config.py` next to `wsgi.py`.

```bash
$ cd PSIRT
$ touch config.py
```

4. Open `config.py` and paste the following snippet.

> To register a Cisco PSIRT OpenVuln API application on Cisco API Console (for `CLIENT_ID` and `CLIENT_SECRET`), follow a long with this [Cisco Guide](https://developer.cisco.com/docs/support-apis/#!application-registration/exploring-the-api-developer-portal) or this [Cisco Community Guide](https://community.cisco.com/t5/services-knowledge-base/accessing-the-cisco-psirt-openvuln-api-using-curl/ta-p/3652897)

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
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    APP_ENV = "production"
    DEBUG = False
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_STORAGE_URI = "mongodb://localhost:27017" # change to Redis or Memcached depending on your choice
    RATELIMIT_IN_MEMORY_FALLBACK_ENABLED = True
    RATELIMIT_KEY_PREFIX = "PSI"
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

7. If deployed in production, change the following line in `__init__.py`

```python
...

def create_app(config_class=ProductionConfig):  # this line
    app = Flask(__name__)
    ...
```

## Documentation

Pointer to reference documentation for this project.

1. [Cisco PSIRT OpenVuln API Documentation](https://developer.cisco.com/docs/psirt/)
2. [API Reference](https://developer.cisco.com/docs/psirt/#!api-reference)
3. [PSIRT Knowledge Base](https://devnetsupport.cisco.com/hc/en-us/sections/115002851487-openVuln-API)

## Disclaimer

Code provided as-is. No warranty implied or included. Use the code for production at your own risk.