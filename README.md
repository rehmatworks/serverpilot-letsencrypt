# rwssl - Let's Encrypt Automation for ServerPilot
This Python utility allows you to automate the installation/uninstallation of SSL certificates from Let's Encrypt on ServerPilot servers. Both free servers (from old grand-fathered plan) and servers on premium plans are supported.

## Donations
Donations always remind me that my program is needed and appreciated by the community. You can [**buy me a coffee here**](https://buymeacoffee.com/rehmat) if you really liked my work. This helps and encourages me to dedicate time for open source projects.

## Getting Started

**If you are upgrading from an older version, first uninstall the older version completely before installing the latest version.**

`pip3 uninstall rwssl`

`pip uninstall rwssl`

And then proceed to the installation. Recommended way to install **rwssl** is via PIP.

If PIP isn't installed on your system, you need to install it first. In addition to PIP, you need to install some other needed packages as well.

```bash
sudo apt-get -y install python3-pip build-essential libssl-dev libffi-dev python3-dev
```

And then run:

```bash
pip3 install rwssl
```

The alternate way to install **rwssl** is cloning the repository:

```bash
git clone https://github.com/rehmatworks/serverpilot-letsencrypt && cd serverpilot-letsencrypt && python3 setup.py install
```

## Examples:
Here are a few examples to get you started:

#### Install SSL on app foo
```bash
rwssl getcert --app foo
```

Uninstall SSL from the app foo:
```bash
rwssl removecert --app foo
```

## All Available Commands
Once **rwssl** is installed, a command `rwssl` will become available in your terminal. You will have access to the following sub-commands in order to manage your server.

| Sub-command | Details | Examples |
| ------- | --- |
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
