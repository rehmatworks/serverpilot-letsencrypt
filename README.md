# ServerPilot Let's Encrypt (`rwssl`) v2.x
This Python utility allows you to automate the installation/uninstallation of SSL certificates from Let's Encrypt on ServerPilot servers. Both free servers (from old grand-fathered plan) and servers on premium plans are supported.

## Donations
Donations always remind me that my program is needed and appreciated by the community. You can [**buy me a coffee here**](https://buymeacoffee.com/rehmat) if you really liked my work. This helps and encourages me to dedicate time for open source projects.

## Getting Started

**If you are using my VERY old bash script, you will have to delete it completely first from `/usr/local/bin/rwssl`.**

Sign in as root user (or with sudo privileges) and install some needed packages:

```bash
sudo apt-get update && apt-get -y install python3-pip build-essential libssl-dev libffi-dev python3-dev
```

And then install the package from PyPi:

```bash
pip3 install --upgrade --force-reinstall rwssl
```

The alternate way to install **rwssl** is by cloning the repository:

```bash
git clone https://github.com/rehmatworks/serverpilot-letsencrypt && cd serverpilot-letsencrypt
pip3 install -r requirements.txt
python3 setup.py install
```

**Only Python 3.5 and up supported.**

## Available Commands with Examples:

Once **rwssl** is installed, a command `rwssl` will become available in your terminal. You will have access to the following sub-commands in order to manage your server.

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

That's all!

## Bugs & Suggestions
Although you should never encounter any security-related issues, but still if you find a security-related issue, please drop an email at contact[at]rehmat.works. For other common issues, you can use the issues section in this repo directly.
