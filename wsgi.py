from psiapp import create_app

__author__ = "Osama Abbas <Osama_Mohamed@seegypt.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "BSD 3-Clause License"

app = create_app()

if __name__ == "__main__":
    app.run()
