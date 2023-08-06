# 🏃 JPL EDRN DMCC Password Relay

This package provides a simple, safe server that listens for usernames and password for the [Early Detection Research Network](https://edrn.nci.nih.gov/)'s Data Management and Coordinating Center's so-called "secure site". It uses the center's antique [SOAP](http://keithba.net/simplicity-and-utility-or-why-soap-lost) service to check those passwords, then gives back a single byte response indicating if the password's valid.

It's intended to be used with [dmccauth](https://github.com/EDRN/dmccauth), an [overlay](https://www.openldap.org/doc/admin26/overlays.html) to [OpenLDAP](https://www.openldap.org/)'s standalone [slapd](https://www.openldap.org/doc/admin26/intro.html#What%20is%20slapd%20and%20what%20can%20it%20do) server. OpenLDAP overlays must be programmed in C and use dynamically-loaded objects, but [SOAP implementations for C](https://www.genivia.com/products.html#gsoap) are available only as static APIs.

With this running alongside OpenLDAP and the `dmccauth` overlay, we can overcome this problem.


## 💽 Installation

This software requires Python 3. Python 3.9 or later is recommended, but Python 4 is not. Typically, you'll make a virtual environment and install the software with a litany like:

    python3 -m venv password-relay
    cd password-relay
    bin/pip install --upgrade --quiet setuptools wheel pip
    bin/pip install password-relay==X.Y.Z

where `X.Y.Z` is the version you want. To upgrade an existing installation, add `--upgrade`. You can then start the server:

    bin/dmcc-passwordrelay

By default, the server creates its listening socket in `/tmp/dmcc.socket`. You can customize that with `--socket`. Try `--help` for all the options.


### 🩺 Testing

You can see if it's working correctly by running the following from another session:

    printf 'USERNAME\PASSWORD\n' | nc -U /tmp/dmcc.socket | more

Replace `USERNAME` and `PASSWORD` and the socket path if necessary. You'll see a `1` for a valid password, or `0` for invalid.


### 😈 Daemonizing

The software runs in the foreground and should always be running. However, it supports no automatic restart. For that, it's recommended you run it under [Supervisord](http://supervisord.org):

    bin/pip install supervisor

Then make a `supervisord.conf` similar to the following:

    [supervisord]
    logfile = %(here)s/var/log/supervisor.log
    logfile_backups = 3
    loglevel = debug
    pidfile = %(here)s/var/supervisor.pid

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [unix_http_server]
    file = %(here)s/var/sockets/supervisor

    [supervisorctl]
    serverurl = unix:%(here)s/var/sockets/supervisor

    [program:passwordrelay]
    command = %(here)s/.venv/bin/dmcc-passwordrelay --socket %(here)s/var/sockets/dmcc
    autorestart = true


## 🔧 Development

To develop this locally, try the following:

    git clone https://github.com/EDRN/jpl.edrn.dmcc.passwordrelay
    cd jpl.edrn.dmcc.passwordrelay
    python3 -m venv venv
    venv/bin/pip install --upgrade --silet setuptools build dist wheel
    vnev/bin/pip install --editable .


### 👥 Contributing

You can start by looking at the [open issues](https://github.com/EDRN/jpl.edrn.ldap.sync/issues), forking the project, and submitting a pull request. You can also [contact us by email](mailto:ic-portal@jpl.nasa.gov) with suggestions.


### 🔢 Versioning

We use the [SemVer](https://semver.org/) philosophy for versioning this software. For versions available, see the [releases made](https://github.com/EDRN/jpl.edrn.ldap.sync/releases) on this project.


## 👩‍🎨 Creators

The principal developer is:

- [Sean Kelly](https://github.com/nutjob4life)


## 📃 License

The project is licensed under the [Apache version 2](LICENSE.md) license.
