#!/bin/bash -   
#title          :rwssl.sh
#description    :A tiny script to automate the installation of Let's Encrypt SSL on ServerPilot servers.
#author         :Rehmat Alam
#date           :20171108
#version        :2.1
#usage          :./rwssl.sh
#============================================================================

if [[ $EUID -ne 0 ]]
	then
   echo -e "\e[33mYou aren't root. Permission issues may arise.\e[39m"
fi

printf "What do you want to do with Let's Encrypt? (install/uninstall): " ; read -r theAction
if [ -z "$theAction" ]
	then
	echo -e "\e[31mPlease specify the task. Should be either install or uninstall\e[39m"
	exit
else
	if [[ ! $theAction =~ ^(install|uninstall)$ ]] 
		then
		echo -e "The task should be either \e[31minstall\e[39m or \e[31muninstall\e[39m"
		exit
	fi
fi

printf "Enter your domain name (Don't include www): " ; read -r domainName
if [ -z "$domainName" ]
	then
	echo -e "\e[31mPlease provide the domain name\e[39m"
	exit
fi

printf "Enter your ServerPilot app name: " ; read -r appName
if [ -z "$appName" ]
	then
	echo -e "\e[31mPlease provide the app name\e[39m"
	exit
fi

printf "Is this a main domain or sub-domain? (main/sub): " ; read -r domainType

spAppRoot="/srv/users/serverpilot/apps/$appName"
spAppPublicRoot="$spAppRoot/public"
spSSLDir="/etc/nginx-sp/vhosts.d/"

# Install Let's Encrypt libraries if not found
if ! hash certbot 2>/dev/null; then
	echo -e "\e[33mLet's Encrypt libs not found. Installing the libraries....\e[39m"
	sudo apt-get update &>/dev/null &&
		yes | sudo apt-get install software-properties-common &>/dev/null &&
		yes | sudo add-apt-repository ppa:certbot/certbot &>/dev/null &&
		yes | sudo apt-get update &>/dev/null &&
		yes | sudo apt-get install certbot &>/dev/null
fi

if [ ! -d "$spAppRoot" ]
	then
	echo -e "\e[31mThe app name seems invalid as we didn't find its directory on your server\e[39m"
	exit 
fi

if [ "$theAction" == "uninstall" ]; then
	sudo rm "$spSSLDir$appName-ssl.conf" &>/dev/null
	sudo service nginx-sp reload
	echo -e "\e[31mSSL has been removed. If you are seeing errors on your site, then please fix HTACCESS file and remove the rules that you added to force SSL\e[39m"
elif [ "$theAction" == "install" ]; then
	if [ -z "$domainType" ]
		then
		echo -e "\e[31mPlease provide the type of the domain (either main or sub)\e[39m"
		exit
	else
		if [[ ! $domainType =~ ^(main|sub)$ ]]
			then
			echo -e "The domain type should be either \e[31main\e[39m or \e[31msub\e[39m"
			exit
		fi
	fi
	echo -e "\e[32mReady to install, press enter to continue\e[39m"
	if [ "$domainType" == "main" ]; then
		thecommand="certbot certonly --webroot -w $spAppPublicRoot --register-unsafely-without-email --agree-tos -d $domainName -d www.$domainName"
	elif [[ "$domainType" == "sub" ]]; then
		thecommand="certbot certonly --webroot -w $spAppPublicRoot --register-unsafely-without-email --agree-tos -d $domainName"
	else
		echo -e "\e[31mDomain type not provided. Should be either main or sub\e[39m"
		exit
	fi
	output=$(eval $thecommand 2>&1) | xargs
	
	if [[ "$output" == *"too many requests"* ]]; then
		echo "Let's Encrypt SSL limit reached. Please wait for a few days before obtaining more SSLs for $domainName"
	elif [[ "$output" == *"Congratulations"* ]]; then
	
	if [ "$domainType" == "main" ]; then
		sudo echo "server {
	listen 443 ssl http2;
	listen [::]:443 ssl http2;
	server_name
	$domainName
	www.$domainName
	;

	ssl on;

	ssl_certificate /etc/letsencrypt/live/$domainName/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/$domainName/privkey.pem;

	root $spAppRoot/public;

	access_log /srv/users/serverpilot/log/$appName/dev_nginx.access.log main;
	error_log /srv/users/serverpilot/log/$appName/dev_nginx.error.log;

	proxy_set_header Host \$host;
	proxy_set_header X-Real-IP \$remote_addr;
	proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
	proxy_set_header X-Forwarded-SSL on;
	proxy_set_header X-Forwarded-Proto \$scheme;

	include /etc/nginx-sp/vhosts.d/$appName.d/*.nonssl_conf;
	include /etc/nginx-sp/vhosts.d/$appName.d/*.conf;
}" > "$spSSLDir$appName-ssl.conf"

	elif [ "$domainType" == "sub" ]; then
		sudo echo "server {
	listen 443 ssl http2;
	listen [::]:443 ssl http2;
	server_name
	$domainName
	;

	ssl on;

	ssl_certificate /etc/letsencrypt/live/$domainName/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/$domainName/privkey.pem;

	root $spAppPublicRoot;

	access_log /srv/users/serverpilot/log/$appName/dev_nginx.access.log main;
	error_log /srv/users/serverpilot/log/$appName/dev_nginx.error.log;

	proxy_set_header Host \$host;
	proxy_set_header X-Real-IP \$remote_addr;
	proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
	proxy_set_header X-Forwarded-SSL on;
	proxy_set_header X-Forwarded-Proto \$scheme;

	include /etc/nginx-sp/vhosts.d/$appName.d/*.nonssl_conf;
	include /etc/nginx-sp/vhosts.d/$appName.d/*.conf;
}" > "$spSSLDir$appName-ssl.conf"
	fi
		echo -e "\e[32mSSL should have been installed for $domainName with auto-renewal (via cron)\e[39m"
		
	elif [[ "$output" == *"Failed authorization procedure."* ]]; then
		echo -e "\e[31m$domainName isn't being resolved to this server. Please check and update the DNS settings if necessary and try again when domain name points to this server\e[39m"
	elif [[ ! $output ]]; then
		# If no output, we will check if SSL is already issued and if so
		# we will just add the vhost
		if [ -f "/etc/letsencrypt/live/$domainName/fullchain.pem" ] && [ -f "/etc/letsencrypt/live/$domainName/privkey.pem" ]; then
			sudo echo "server {
		listen 443 ssl http2;
		listen [::]:443 ssl http2;
		server_name
		$domainName
		www.$domainName
		;

		ssl on;

		ssl_certificate /etc/letsencrypt/live/$domainName/fullchain.pem;
		ssl_certificate_key /etc/letsencrypt/live/$domainName/privkey.pem;

		root $spAppPublicRoot;

		access_log /srv/users/serverpilot/log/$appName/dev_nginx.access.log main;
		error_log /srv/users/serverpilot/log/$appName/dev_nginx.error.log;

		proxy_set_header Host \$host;
		proxy_set_header X-Real-IP \$remote_addr;
		proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-SSL on;
		proxy_set_header X-Forwarded-Proto \$scheme;

		include /etc/nginx-sp/vhosts.d/$appName.d/*.nonssl_conf;
		include /etc/nginx-sp/vhosts.d/$appName.d/*.conf;
	}" > "$spSSLDir$appName-ssl.conf"
		echo -e "\e[32mSSL should have been installed for $domainName with auto-renewal (via cron)\e[39m"
		else
			echo -e "\e[31mSSL cannot be obtained at the moment. Please try again.\e[39m"
		fi
	else
		echo -e "\e[31mSomething unexpected occurred\e[39m"
	fi 
	sudo service nginx-sp reload
else
	echo -e "\e[31mTask cannot be identified. It should be either install or uninstall \e[39m"
fi
