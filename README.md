# Let's Encrypt on Your ServerPilot Free Plan
Automate the installation of Let's Encrypt SSL on the free plan of ServerPilot

## About the script
ServerPilot's paid plan costs only $10 per month that unlocks auto installation of Let's Encrypt SSL along with some other premium features. But if you don't want to spend that $10 then this script can automate the installation of the SSL on your ServerPilot servers. When you activate the SSL for an app, this script adds a cron job as well that takes care of the renewal of your Let's Encrypt SSL.

## Getting started

#### Step 1: Clone the repo
If git isn't installed on your system, then install it first by typing this in terminal
```bash
  sudo apt-get -y install git
```
and then run this command to clone the reposity
```bash
sudo git clone https://github.com/rehmatworks/serverpilot-letsencrypt/ && cd serverpilot-letsencrypt && sudo mv sple.sh /usr/local/bin/rwssl && sudo chmod +x /usr/local/bin/rwssl
```
When you will run the above command, the repo will be cloned to your system and the script will be copied to /usr/local/bin and will be made executable. After that, you can execute it easily.

## Install SSL
Here are the simple steps to install SSL on your apps
#### For main domains (Don't include www with your domain)
```bash
rwssl install example.com app_name main
```
In above example, you can see that I've passed four arguments to rwssl command. The first argument tells the script to install the SSL. Second argument is the domain name. Third argument is the app name of your domain and fourth argument tells either this is a sub domain or the main domain.

### For sub domains
```bash
rwssl install sub.example.com app_name sub
```

## Uninstall SSL
```bash
rwssl uninstall example.com
```
```bash
rwssl uninstall sub.example.com
```
Any questions? Ask me in my blog post [here](https://rehmat.works/install-lets-encrypt-on-the-free-plan-of-serverpilot/).
