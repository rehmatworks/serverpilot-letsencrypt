# ServerPilot Let's Encrypt (`rwssl`) v2.x
This Python utility allows you to automate the installation/uninstallation of SSL certificates from Let's Encrypt on ServerPilot servers. Both free servers (from old grand-fathered plan) and servers on premium plans are supported.

![serverpilot-letsencrypt](https://raw.githubusercontent.com/rehmatworks/serverpilot-letsencrypt/master/rwssl.png "ServerPilto Let's Encrypt")

## Getting Started

First of all, sign in as root user (or with sudo privileges). Now remove the very old script if you are still using it:

```bash
rm /usr/local/bin/rwssl
```

And then install some needed packages:

```bash
apt-get update  && \
apt-get -y install python3-pip build-essential libssl-dev libffi-dev python3-dev
```

Uninstall older version if exists:
```bash
pip3 uninstall -y rwssl
```

And then install the latest version from PyPi:

```bash
pip3 install rwssl==2.0.4
```

Verify that the installation worked. This should bring up the help menu for **rwssl**:

```bash
rwssl -h
```

The alternate way to install **rwssl** is by cloning the repository:

```bash
cd ~/ && \
git clone https://github.com/rehmatworks/serverpilot-letsencrypt  && \
cd serverpilot-letsencrypt && \
pip3 install -r requirements.txt && \
python3 setup.py install
```

Only Python 3.5 and up supported so you shoul install & use rwssl package using pip3 and Python 3.x.

## Available Commands with Examples:

Once **rwssl** is installed, a command `rwssl` will become available in your terminal. You will have access to the following sub-commands in order to manage your server.

**Update:** Please note that old commands aren't available anymore due to a recent major upgrade. Please check below table for new commands that come with rwssl. You can get help by typing `rwssl -h` as well.

| Command | Details | Examples |
| ------- | --- | -- |
| getcert | Get letsencrypt cert for an app. | `rwssl getcert --app foo` |
| getcerts | Get letsencrypt certs for all apps. | `rwssl getcerts` for all users apps or `rwssl getcerts --user john` for john's apps |
| removecert | Uninstall SSL cert from an app. | `rwssl removecert --app foo` |
| removecerts | Uninstall SSL certs for all apps. | `rwssl removecerts` for all users apps or `rwssl removecerts --user john` for john's apps |
| forcessl | Force SSL certificate for an app. | `rwssl forcessl --app foo` |
| unforcessl | Unforce SSL certificate for an app. | `rwssl unforcessl --app foo` |
| forceall | Force HTTPs for all apps. | `rwssl forceall` for all users apps or `rwssl forceall --user john` for john's apps |
| unforceall | Unforce HTTPs for all apps. | `rwssl unforceall` for all users apps or `rwssl unforceall --user john` for john's apps |

You can use `rwssl -h` command to get to the help page on above commands.

## Uninstall
To uninstall rwssl completely, run:
```bash
pip3 uninstall rwssl
```

As a CRON job is added for SSL renewals by rwssl, you can remove the CRON file by running:

```bash
rm /etc/cron.weekly/rwssl-sslrenewals
```

Moreoever, a conf file `acme.conf` is created in conf directory of each app in vhosts.d. You should delete them as well. For example, if your app name is example, you should delete the conf file `/etc/nginx-sp/vhosts.d/example.d/acme.conf`. Repeat this step for each app where you used rwssl to get the SSL certificates.

That's all!

## Changelog

## [2.0.0] - 2020-04-18
A major upgrade that addresses all reported bugs including SSL renewals.

### Changes
- Custom path is used to store SSL certificates
- Certificate is named after app name (Addresses missing cert path issue)
- Improved vhost file parsing to get app details
- Dropped support for Python 2.x (Only Python 3.x is supported)
- Using Let's Encrypt staging server (via dry-run) for domain validation (To address quota issues)

### Added
- Using Jinja template engine to generate virtual host files from templates
- Using a custom ACME verification location (To avoid initial verifications & renewal issues)
- Using latest certbot Python package
- ACME v2 protocol support
- Added validation after vhost files are written (and changes are reverted if errors encountered)

## Bugs & Suggestions
For security-related issues, please email me at **contact@rehmat.works** and for common bug reports / feature requests, use the issues section.
