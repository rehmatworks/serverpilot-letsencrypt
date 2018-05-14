# Let's Encrypt on Your ServerPilot Free Plan
Automate the installation of Let's Encrypt SSL on the free plan of ServerPilot
#### Update: Now ***rwssl*** can install SSLs for all apps at once with a single command `rwssl -a`

## Getting started

#### Install 
```bash
pip install rwssl
```
PIP not installed? Install it by running `apt-get install python-pip`

#### Upgrade
If you have used `rwssl` previously on a server, then follow these instructions:

1. Remove old script
```bash
rm /usr/local/bin/rwssl
```

2. Install the latest package
```bash
pip install rwssl
```

If all goes fine, a new command `rwssl` will become available.

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

### Renew SSLs
```bash
rwssl -r
```
or

```bash
rwssl --renew
```

### Install CRON Job for SSL Renewals
```bash
rwssl -ic
```
or

```bash
rwssl --installcron
```

To get help on commands, type `rwssl -h` or `rwssl --help`

Any questions? Ask me in my blog post [here](https://rehmat.works/install-lets-encrypt-on-the-free-plan-of-serverpilot/).

## How to Uninstall
To unintall `rwssl`, simply delete the script:
```bash
sudo rm /usr/local/bin/rwssl
```
Lastly, edit the crontab by running `crontab -e` command and delete the added CRON jobs responsible for SSL auto-renewals.