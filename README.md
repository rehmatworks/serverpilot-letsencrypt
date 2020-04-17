# SP Suite (for ServerPilot)
SP Suite is a Python library written to interact with ServerPilot-managed servers over CLI. If you want to manage your ServerPilot server over command line, this utility is for you.

## Donations
Donations always remind me that my program is needed and appreciated by the community. You can [**buy me a coffee here**](https://buymeacoffee.com/rehmat) if you really liked my work. This helps and encourages me to dedicate time for open source projects.

## Getting Started
Recommended way to install SP Suite is via PIP.

If PIP isn't installed on your system, you need to install it first. In addition to PIP, you need to install some other needed packages as well.

```bash
sudo apt-get -y install python3-pip build-essential libssl-dev libffi-dev python3-dev
```

And then run:

```bash
pip3 install spsuite
```

The alternate way to install SP Suite is cloning the repository:

```bash
git clone https://github.com/rehmatworks/spsuite && cd spsuite && python3 setup.py install
```

## Examples:
Here are a few examples to get you started:

#### List Apps
To list all apps owned by all users on the server, use:
```bash
spsuite listapps
```

And to list apps for a specific SSH user, use:
```bash
spsuite listapps --user johndoe
```

#### Create an App
To create a new app, use `createapp` command:
```bash
spsuite createapp --name myapp --user johndoe --php 7.4 --domains example.com,www.example.com
```
Above command will create an app under SSH user **johndoe** with PHP version **7.4** and with domains **example.com** and **www.example.com**. If the SSH user **johdoe** is not present, it will be created first.

#### Delete an App
To delete an app permanently, use this command. Remember that all associated data will be permanently deleted.
```bash
spsuite deleteapp --name myapp
```

These are just a few commands as examples. In below table, you can get the list of all available commands.

## All Available Commands
Once SP Suite is installed, a command `spsuite` will become available in your terminal. You will have access to the following sub-commands in order to manage your server.

| Sub-command | Details |
| ------- | --- |
| listsysusers | Show all SSH users existing on this server. |
| createsysuser | Create a new SSH user. |
| listapps | Show all existing apps. |
| createapp | Create a new app. |
| updatedomains | Update an apps' domains and recreate vhost files. |
| changephp | Change PHP version of an app. |
| changephpall | Change PHP version for all apps. |
| deleteapp | Delete an app permanently. |
| delallapps | Delete all apps permanently. |
| listdbusers | Show all existing database users. |
| createsqluser | Create a new MySQL user. |
| updatesqlpassword | Update any MySQL user's password. |
| dropuser | Drop a MySQL user. |
| dropallsqlusers | Drop all MySQL users except system users (root, sp-admin, debian-sys-maint, mysql.session, mysql.sys). |
| listdbs | Show all existing databases. |
| createdb | Create a new MySQL database. |
| dropdb | Drop a MySQL database. |
| dropalldbs | Drop all databases except system databases (information_schema, mysql, performance_schema, sys). |
| getcert | Get letsencrypt cert for an app. |
| getcerts | Get letsencrypt certs for all apps. |
| removecert | Uninstall SSL cert from an app. |
| removecerts | Uninstall SSL certs for all apps. |
| forcessl | Force SSL certificate for an app. |
| unforcessl | Unforce SSL certificate for an app. |
| forceall | Force HTTPs for all apps. |
| unforceall | Unforce HTTPs for all apps. |
| denyunknown | Deny requests from unknown domains. |
| allowunknown | Allow requests from unknown domains. |

You can use `spsuite -h` command to get to the help page on above commands.

## Uninstall
To uninstall SP Suite completely, run:
```bash
pip3 uninstall spsuite
```

As a CRON job is added for SSL renewals by SP Suite, you can remove the CRON file by running:

```bash
rm /etc/cron.weekly/spsuite-sslrenewals
```

That's all!

## Bugs & Suggestions
Although you should never encounter any security-related issues, but still if you find a security-related issue, please drop an email at contact[at]rehmat.works. For other common issues, you can use the issues section in this repo directly.
