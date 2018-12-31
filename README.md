<a href="https://www.buymeacoffee.com/Z0Mitv3HA" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

# Let's Encrypt on Your ServerPilot Servers
Automate the installation of Let's Encrypt SSL on servers managed by ServerPilot. Both free and paid plans of ServerPilot are supported now. SSLs can be installed on all apps owned by serverpilot or any other user.

Update: Now ***rwssl*** can install SSLs for all apps at once with a single command `rwssl -a`

### Attention: All Prevoious Versions Need an Upgrade
In order to get SSL renewals work flawlessly, all versions prior to v1.0.3 need an upgrade. If you are using the old script and haven't installed it using Python PIP, then please scroll to the bottom of this page to learn how to upgrade. If you have installed the package using PIP, then check `rwssl` version like this:
```bash
pip show rwssl
```
If the version is older than 1.0.5, then you need to upgrade it:
```bash
pip uninstall rwssl
pip install --no-cache-dir rwssl
```

## Getting started

#### Install 
```bash
pip install rwssl
```
PIP not installed? Install it by running:
```bash
apt install python-pip
```

If all goes fine, a new command `rwssl` will become available.

Below commands can be used with `rwssl`:

#### Available Commands
```
  -h, --help            show this help message and exit
  -a, --all             Install SSL for all available apps.
  -f, --fresh           Obtain and install SSL certificates for new (non-ssl)
                        apps only.
  -i IGNOREAPPS, --ignore IGNOREAPPS
                        Comma-seperated app names to ignore some apps and
                        install SSL for all others.
  -n APPNAME, --name APPNAME
                        Name of the app where SSL should be installed.
  -r, --renew           Renew all installed SSL certificates which are about
                        to expire.
  -ic, --installcron    Install the cron job for SSL renewals.
  -dc, --deletecron     Uninstall the cron job responsible for SSL renewals.
  -ap, --autopilot      A CRON job that attempts to automatically obtain SSL
                        certificates for newly added apps.
  -na, --noautopilot    Disable Autopilot mode and disable automatic SSLs for
                        your apps.
  -re, --refresh        Cleans all previous SSL vhost files, reinstalls the
                        SSLs and reloads nginx. Only needed if you are having
                        issues on a server with old SSL installations.
  -redir REDIRECT, --redirect REDIRECT
                        Apply a 301 redirect from HTTP to HTTPs for a given
                        app or for all apps.
  -noredir NOREDIRECT, --noredirect NOREDIRECT
                        Disable HTTP to HTTPs redirect for a single app or for
                        all apps.
```

### Get Help on All Available Commands
```bash
rwssl -h
```

or

```bash
rwssl --help
```

### Install SSLs

1. Install SSL on all available apps
```bash
rwssl -a
```
or
```bash
rwssl --all
```

2. Install SSL on all apps ignoring some (Provide comma-separated app names)
```bash
rwssl -i 'app1,app2,app3'
```
or
```bash
rwssl --ignore 'app1,app2,app3'
```
3. Install SSL on a specific app
```bash
rwssl -n app_name
```

4. Install SSL on all new apps (that doesn't have an SSL yet)
```bash
rwssl -f
```
or
```bash
rwssl --fresh
```

### Renew SSLs
```bash
rwssl -r
```
or

```bash
rwssl --renew
```

### CRON Job for SSL Renewals
Install the CRON job:
```bash
rwssl -ic
```
or

```bash
rwssl --installcron
```

Uninstall the CRON job (Renewals will not be carried out by `rwssl`):
```bash
rwssl -dc
```
or

```bash
rwssl --deletecron
```

### Autopilot Mode
Enable autopilot mode so you will not need to obtain SSL certificates for your new apps manually. This will add a CRON job set to run every `10 minutes`. `rwssl` will check for new non-ssl apps and if any new apps are added, an SSL certificate will be obtained and installed automatically.

Enable Autopilot Mode:
```bash
rwssl -ap
```

or

```bash
rwssl --autopilot
```

Disable Autopilot Mode:
```bash
rwssl -na
```

or

```bash
rwssl --noautopilot
```

### Refresh SSL Apps:
If you have added SSL vhosts in the past yourself or if you have used the old `rwssl` script, then this command is helpful in order to do a cleanup and reinstall SSL certificates/SSL vhosts. You should not run it unless it is too important.

```bash
rwssl -re
```

or

```bash
rwssl --refresh
```

### Force HTTPS (301 Redirect):
You don't need to modify your `.htaccess` file or `nginx` configuration manually to enable HTTP to HTTPS redirect as `rwssl` does it automatically for you.

To force HTTPS on all apps:
```bash
rwssl -redir all
```

or

```bash
rwssl --redirect all
```

To force HTTPS on a selected app:
```bash
rwssl -redir appname
```

or

```bash
rwssl --redirect appname
```

To disable HTTPS redirect for all apps:
```bash
rwssl -noredir all
```

or

```bash
rwssl -noredirect all
```

To disable HTTPS redirect on a selected app:
```bash
rwssl -noredir appname
```

or

```bash
rwssl -noredirect appname
```

If you notice redirect loops after enabling `HTTP` to `HTTPS` redirect, then it means that either your SSL vhosts need a refresh (`rwssl -re`) or your website's `.htaccess` rules need to be fixed. In such a scenario, please fix your `.htaccess` file or disable the SSL for the app by running `rwssl -noredir appname` until you sort out the issue.

#### Upgrade (Only for old script's users)
If you have used `rwssl` previously on a server, then follow these instructions:

1. Remove old script
```bash
rm /usr/local/bin/rwssl
```

2. Install the latest package
```bash
pip install rwssl
```

To get help on commands, type `rwssl -h` or `rwssl --help`

Any questions? Ask me in my blog post [here](https://rehmat.works/install-lets-encrypt-on-the-free-plan-of-serverpilot/).

## How to Uninstall
To unintall `rwssl`, simply run:
```bash
sudo pip uninstall rwssl
```
