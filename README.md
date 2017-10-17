# Let's Encrypt on Your ServerPilot Free Plan
Automate the installation of Let's Encrypt SSL on the free plan of ServerPilot

## About the script
ServerPilot's paid plan costs only $10 per month that unlocks auto installation of Let's Encrypt SSL along with some other premium features. But if you don't want to spend that $10 then this script can automate the installation of the SSL on your ServerPilot servers. When you activate the SSL for an app, this script adds a cron job as well that takes care of the renewal of your Let's Encrypt SSL.

## Getting started

#### Step 1: Clone the repo
Run this command to clone the reposity and to add the CRON job for auto-renewal of the certs:
```bash
sudo git clone https://github.com/rehmatworks/serverpilot-letsencrypt.git && cd serverpilot-letsencrypt && sudo mv sple.sh /usr/local/bin/rwssl && sudo chmod +x /usr/local/bin/rwssl && (crontab -l ; echo "@monthly \"sudo service nginx-sp stop && yes | letsencrypt renew &>/dev/null && service nginx-sp start && service nginx-sp reload\"")| crontab - && service cron reload
```
If git isn't installed on your system and you get error while executing above command, then install it first by typing this in terminal
```bash
  sudo apt-get -y install git
```

Successful execution of the above command will clone the script to your system and the script will be copied to /usr/local/bin and will be made executable as **rwssl**. After that, you can execute it easily by running **rwssl** command.

## Install SSL
In the latest version of this script, installation has been made super-simple. You don't need to pass arguments along with the command. Simply run the command **rwssl** and it will ask you for the required information and the SSL will be installed on your system after a few quick steps.
```bash rwssl```
Any questions? Ask me in my blog post [here](https://rehmat.works/install-lets-encrypt-on-the-free-plan-of-serverpilot/).
