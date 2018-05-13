#! /usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os
import nginx
import argparse

# Argument parsing
ap = argparse.ArgumentParser(description='A Python script that automates the SSL installation on ServerPilot free servers.')
ap.add_argument('-d', '--domain', dest='domain', help='Domain name of the app', default=False)
ap.add_argument('-r', '--root', dest='root', help='Root directory of the app excluding public', default=False)
ap.add_argument('-a', '--all', dest='all', help='Install SSL for all available apps.', action='store_const', const=True, default=False)
ap.add_argument('-n', '--name', dest='appname', help='Name of the app.', default=False)

args = ap.parse_args()
vhostsdir = '/etc/nginx-sp/vhosts.d/' # ServerPilot vhosts directory
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def find_between(s, first, last):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return None

def apps():
	spapps = []
	for file in os.listdir(vhostsdir):
		if file.endswith(".conf"):
			conf_file = os.path.join(vhostsdir, file)
			c = nginx.loadf(conf_file).as_dict
			def search(value):
				data = c.get('conf')
				for conf in data:
					blocks = conf.get('server')
					for block in blocks:
						found = block.get(value)
						if found:
							return found
				return None
			try:
				domains = search('server_name').split() # All app domains
			except:
				domains = None
			try:
				root = search('root')
			except:
				root = None
			try:
				appname = find_between(root, 'apps/', '/')
			except:
				appname = None
			if(appname and domains and root):
				domaininfo = {'domains': domains, 'root': root, 'appname': appname}
				spapps.append(domaininfo)
	return spapps

def certbot_command(root, domains):
	domainsstr = ''
	for domain in domains:
		domainsstr += ' -d '+domain
	cmd = "certbot certonly --webroot -w "+root+" --register-unsafely-without-email --agree-tos"+domainsstr+ " 2>&1"
	return cmd

def write_conf(app):
	print(bcolors.OKBLUE+'Writing NGINX vhost file for the app '+bcolors.BOLD+app.get('appname')+bcolors.ENDC)
	appname = app.get('appname')
	root = app.get('root')
	confname = vhostsdir + appname + '-ssl.conf'
	domains = app.get('domains')
	c = nginx.Conf()
	s = nginx.Server()
	s.add(
		nginx.Comment('SSL conf added by rwssl (https://github.com/rehmatworks/serverpilot-letsencrypt)'),
		nginx.Key('listen', '443 ssl http2'),
		nginx.Key('listen', '[::]:443 ssl http2'),
		nginx.Key('server_name', ' '.join(domains)),
		nginx.Key('ssl', 'on'),
		nginx.Key('ssl_certificate', '/etc/letsencrypt/live/'+domains[0]+'/fullchain.pem'),
		nginx.Key('ssl_certificate_key', '/etc/letsencrypt/live/'+domains[0]+'/privkey.pem'),
		nginx.Key('root', root),
		nginx.Key('access_log', '/srv/users/serverpilot/log/'+appname+'/dev_nginx.access.log main'),
		nginx.Key('error_log', '/srv/users/serverpilot/log/'+appname+'/dev_nginx.error.log'),
		nginx.Key('proxy_set_header', 'Host $host'),
		nginx.Key('proxy_set_header', 'X-Real-IP $remote_addr'),
		nginx.Key('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'),
		nginx.Key('proxy_set_header', 'X-Forwarded-SSL on'),
		nginx.Key('proxy_set_header', 'X-Forwarded-Proto $scheme'),
		nginx.Key('include', '/etc/nginx-sp/vhosts.d/'+appname+'.d/*.nonssl_conf'),
		nginx.Key('include', '/etc/nginx-sp/vhosts.d/'+appname+'.d/*.conf'),
	)
	c.add(s)
	try:
		nginx.dumpf(c, confname)
		print(bcolors.OKGREEN+'Virtual host file created!'+bcolors.ENDC)
		print(bcolors.OKBLUE+'Reloading NGINX server...'+bcolors.ENDC)
		os.system('sudo service nginx-sp reload  &>/dev/null')
		print(bcolors.OKGREEN+'SSL should have been installed and activated for the app'+bcolors.BOLD+app.get('appname')+bcolors.ENDC)
		return True
	except:
		print(bcolors.FAIL+'Virtual host file cannot be created!'+bcolors.ENDC)
		return False

def install_certbot():
	return 'sudo apt-get update &>/dev/null && yes | sudo apt-get install software-properties-common &>/dev/null && yes | sudo add-apt-repository ppa:certbot/certbot &>/dev/null && yes | sudo apt-get update &>/dev/null && yes | sudo apt-get install certbot &>/dev/null'

def get_ssl(app):
	if(os.path.isdir(app.get('root'))):
		domains = app.get('domains')
		cmd = certbot_command(app.get('root'), domains)
		cboutput = os.popen(cmd).read()
		if 'Congratulations' in cboutput:
			print(bcolors.OKGREEN+'SSL has been successfully obtained for '+' '.join(domains)+bcolors.ENDC)
			return True
		elif 'Failed authorization procedure' in cboutput:
			print(bcolors.FAIL+'DNS check failed. Please ensure that the domains '+bcolors.BOLD+' '.join(domains)+bcolors.ENDC+bcolors.FAIL+' are resolving to your server.'+bcolors.ENDC)
		elif 'too many requests' in cboutput:
			print(bcolors.WARNING+'SSL limit reached for '+' '.join(domains)+'. Please wait before obtaining another SSL.'+bcolors.ENDC)
		elif 'command not found' in cboutput:
			print(bcolors.WARNING+'Certbot (Let\'s Encrypt libraries) not found. Installing libs.'+bcolors.ENDC)
			install_certbot();
			cboutput = os.popen(cmd).read()
			if 'Congratulations' in cboutput:
				print(bcolors.OKGREEN+'SSL has been successfully obtained for '+' '.join(domains)+bcolors.ENDC)
			else:
				print(bcolors.FAIL+'Something went wrong. SSL cannot be installed for '+bcolors.BOLD+' '.join(domains)+bcolors.ENDC)
	else:
		print(bcolors.FAIL+'Provided path of the app seems to be invalid.'+bcolors.ENDC)
		exit
	return False
if args.all is True:
	apps = apps()
	for app in apps:
		install = get_ssl(app)
		if(install):
			write_conf(app)
else:
	if args.appname and args.domain and args.root:
		app = {'appname': args.appname, 'domains': [args.domain], 'root': args.root}
		install = get_ssl(app)
		if(install):
			write_conf(app)

	else:
		if args.appname is False or args.appname is None:
			print(bcolors.FAIL+'App name cannot be blank.'+bcolors.ENDC)
		if args.domain is False or args.domain is None:
			print(bcolors.FAIL+'Domain name cannot be blank.'+bcolors.ENDC)
		if args.root is False or args.root is None:
			print(bcolors.FAIL+'Root directory of the app cannot be blank.'+bcolors.ENDC)
