#! /usr/bin/env python
# -*- coding: utf-8 -*-
import glob, os, sys
import nginx
import commands
import argparse
# ServerPilot vhosts directory
vhostsdir = '/etc/nginx-sp/vhosts.d/'
# Cron file of rwssl renewal
cronfile = '/etc/cron.d/rwsslrenew'
# Cron file of rwssl autopilot
rwsslcron = '/etc/cron.d/rwssl'

def reload_nginx_sp():
	os.system('sudo service nginx-sp reload')

def find_between(s, first, last):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return None

def search(value, data):
	for conf in data:
		blocks = conf.get('server')
		for block in blocks:
			found = block.get(value)
			if found:
				return found
	return None

def get_conf_files(rootdir):
	if os.path.isdir(rootdir):
		confs = []
		for conf_file in glob.glob(rootdir+'/*.conf'):
			confs.append(conf_file)
		return confs
	return False

def ssl_installed(app):
	vhostfile = os.path.join(vhostsdir + app.get('appname')+'-ssl.conf')
	if os.path.exists(vhostfile):
		return True
	return False

def apps():
	spapps = []
	print(bcolors.HEADER+'Finding apps...'+bcolors.ENDC)
	conf_files = get_conf_files(vhostsdir)
	if conf_files:
		for conf_file in conf_files:
			if '-ssl.conf' not in conf_file:
				appinfo = get_app_info(conf_file)
				if(appinfo):
					spapps.append(appinfo)
	if(len(spapps) > 0):
		print(bcolors.OKBLUE+str(len(spapps))+' apps found in total. Proceeding further...'+bcolors.ENDC)
	else:
		print(bcolors.FAIL+'No apps found. Ensure that you have created some apps already.'+bcolors.ENDC)
	return spapps

def certbot_command(root, domains):
	domainsstr = ''
	for domain in domains:
		domainsstr += ' -d '+domain
	cmd = "certbot certonly --webroot -w "+root+" --register-unsafely-without-email --agree-tos --force-renewal"+domainsstr
	return cmd

def write_conf(app):
	print(bcolors.OKBLUE+'Writing NGINX vhost file for the app '+bcolors.BOLD+app.get('appname')+bcolors.ENDC)
	appname = app.get('appname')
	root = app.get('root')
	username = app.get('username', 'serverpilot')
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
		nginx.Key('access_log', '/srv/users/'+username+'/log/'+appname+'/dev_nginx.access.log main'),
		nginx.Key('error_log', '/srv/users/'+username+'/log/'+appname+'/dev_nginx.error.log'),
		nginx.Key('proxy_set_header', 'Host $host'),
		nginx.Key('proxy_set_header', 'X-Real-IP $remote_addr'),
		nginx.Key('proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'),
		nginx.Key('proxy_set_header', 'X-Forwarded-SSL on'),
		nginx.Key('proxy_set_header', 'X-Forwarded-Proto $scheme'),
		nginx.Key('include', '/etc/nginx-sp/vhosts.d/'+appname+'.d/*.conf'),
	)
	c.add(s)
	try:
		nginx.dumpf(c, confname)
		print(bcolors.OKGREEN+'Virtual host file created!'+bcolors.ENDC)
		print(bcolors.OKBLUE+'Reloading NGINX server...'+bcolors.ENDC)
		reload_nginx_sp()
		print(bcolors.OKGREEN+'SSL should have been installed and activated for the app '+bcolors.BOLD+app.get('appname')+bcolors.ENDC)
		return True
	except:
		print(bcolors.FAIL+'Virtual host file cannot be created!'+bcolors.ENDC)
		return False

def install_certbot():
	return 'sudo apt-get update && yes | sudo apt-get install software-properties-common && yes | sudo add-apt-repository ppa:certbot/certbot && yes | sudo apt-get update && yes | sudo apt-get install certbot'

def get_app_info(conf_file):
	domaininfo = False
	if os.path.exists(conf_file):
		c = nginx.loadf(conf_file).as_dict
		data = c.get('conf')[-1:]
		try:
			domains = search('server_name', data).split() # All app domains
		except:
			domains = None
		try:
			root = search('root', data)
		except:
			root = None
		try:
			appname = find_between(root, 'apps/', '/')
		except:
			appname = None
		try:
			username = find_between(root, 'users/', '/')
		except:
			username = 'serverpilot'
		if(appname and domains and root):
			domaininfo = {'domains': domains, 'root': root, 'appname': appname, 'username': username}
	return domaininfo

def install_sp_cron():
	if(os.path.exists(cronfile)):
		print(bcolors.OKBLUE+'CRON job is already added properly and renewals should work out of the box.'+bcolors.ENDC)
	else:
		try:
			with open(cronfile, 'w') as f:
				f.write("0 */6 * * * root /usr/local/bin/rwssl -r > /dev/null 2>&1\n")
			print(bcolors.OKGREEN+'Cron job has been successfully installed for SSL renewals.'+bcolors.ENDC)
		except:
			print(bcolors.FAIL+'CRON job cannot be added. Please ensure that you have root privileges.'+bcolors.ENDC)

def uninstall_sp_cron():
	if(os.path.exists(cronfile)):
		try:
			os.unlink(cronfile)
			print(bcolors.OKBLUE+'SSL renewal CRON job has been disabled.'+bcolors.ENDC)
		except:
			print(bcolors.OKBLUE+'The CRON job cannot be disabled. Please try again.'+bcolors.ENDC)
	else:
		print(bcolors.OKBLUE+'SSL renewal CRON job is not configured. No action needed.'+bcolors.ENDC)

def renew_ssls():
	cmd = 'certbot renew'
	commands.getstatusoutput(cmd)
	reload_nginx_sp()
	print(bcolors.OKBLUE+'Renewals should have been succeeded for all expiring SSLs.'+bcolors.ENDC)

def get_ssl(app):
	print(bcolors.OKBLUE+'Obtaining SSL certificate for the app '+bcolors.BOLD+app.get('appname')+'.'+bcolors.ENDC)
	if(os.path.isdir(app.get('root'))):
		domains = app.get('domains')
		cmd = certbot_command(app.get('root'), domains)
		cboutput = commands.getstatusoutput(cmd)[1]
		if 'Congratulations' in cboutput:
			print(bcolors.OKGREEN+'SSL certificate has been successfully obtained for '+' '.join(domains)+bcolors.ENDC)
			return True
		elif 'Failed authorization procedure' in cboutput:
			print(bcolors.FAIL+'DNS check failed. Please ensure that the domain(s) '+bcolors.BOLD+' '.join(domains)+bcolors.ENDC+bcolors.FAIL+' are resolving to your server.'+bcolors.ENDC)
		elif 'too many requests' in cboutput:
			print(bcolors.FAIL+'SSL certificates limit reached for '+' '.join(domains)+'. Please wait before obtaining another SSL.'+bcolors.ENDC)
		else:
			print(bcolors.FAIL+'Something went wrong. SSL certificate cannot be installed for '+bcolors.BOLD+' '.join(domains)+bcolors.ENDC)
	else:
		print(bcolors.FAIL+'Provided path of the app seems to be invalid.'+bcolors.ENDC)
		exit
	return False

def do_initial_config():
	checkcertbot = commands.getstatusoutput('certbot')
	errcodes = [32512]
	if checkcertbot[0] in errcodes:
		print(bcolors.OKBLUE+'Required (certbot) libraries not found. Performing initial (one-time) setup...'+bcolors.ENDC)
		certbotcmd = install_certbot();
		commands.getstatusoutput(certbotcmd)
		print(bcolors.OKGREEN+'Finished installing required libraries. Please re-run your previous command now.'+bcolors.ENDC)
		sys.exit()
		
def ssl_status():
	theapps = False
	allapps = apps()
	if(len(allapps) > 0):
		nonssl = []
		sslapps = []
		for app in allapps:
			if(ssl_installed(app)):
				sslapps.append(app)
			else:
				nonssl.append(app)
		theapps = {'ssl': sslapps, 'nonssl': nonssl}
	return theapps

def do_final_ssl_install(app):
	install = get_ssl(app)
	if(install):
		write_conf(app)

def add_autopilot_cron():
	if(os.path.exists(rwsslcron)):
		print(bcolors.OKBLUE+'Autopilot CRON job is already added and it should be working out of the box.'+bcolors.ENDC)
	else:
		try:
			with open(rwsslcron, 'w') as f:
				f.write("*/10 * * * * root /usr/local/bin/rwssl -f > /dev/null 2>&1\n")
			print(bcolors.OKGREEN+'Autopilot CRON job has been added and now SSL certs should get installed on your new apps automatically.'+bcolors.ENDC)
		except:
			print(bcolors.FAIL+'Autopilot CRON job cannot be added. Please ensure that you have root privileges.'+bcolors.ENDC)

def disable_autopilot_cron():
	if(os.path.exists(rwsslcron)):
		try:
			os.unlink(rwsslcron)
			print(bcolors.OKBLUE+'Autopilot CRON job has been disabled.'+bcolors.ENDC)
		except:
			print(bcolors.FAIL+'An error occured while disabling Autopilot CRON.'+bcolors.ENDC)
	else:
		print(bcolors.OKBLUE+'Autopilot CRON job is not configured yet. No action needed.'+bcolors.ENDC)

def refresh_ssl_apps():
	confs = get_conf_files(vhostsdir)
	sslapps = []
	if confs:
		for conf in confs:
			if 'ssl.conf' in conf:
				appinfo = get_app_info(conf)
				if appinfo:
					sslapps.append(appinfo)
				print(bcolors.FAIL+'Deleting SSL vhost '+conf+bcolors.ENDC)
				os.unlink(conf)
		if(len(sslapps) > 0):
			print(bcolors.OKBLUE+'Refreshing SSL certificates for '+str(len(sslapps))+' apps. Obsolete vhosts will be cleaned.'+bcolors.ENDC)
			for app in sslapps:
				do_final_ssl_install(app)
		else:
			print(bcolors.FAIL+'No apps need to be refreshed.'+bcolors.ENDC)

def app_conf_dir(app):
	conf_dir = os.path.join(vhostsdir, app.get('appname')+'.d/')
	if(os.path.isdir(conf_dir)):
		return conf_dir
	else:
		return False

def app_custom_conf(app):
	conf_dir = app_conf_dir(app)
	if conf_dir:
		return os.path.join(conf_dir, 'rwssl.nonssl_conf')
	return False

def force_ssl(app):
	conf_file = app_custom_conf(app)
	if(conf_file):
		try:
			with open(conf_file, 'w') as f:
				f.write("return 301 https://$host$request_uri;")
			print(bcolors.OKBLUE+'HTTP to HTTPS redirect configuration file has been written successfully.'+bcolors.ENDC)
			print(bcolors.OKBLUE+'Reloading NGINX server...'+bcolors.ENDC)
			reload_nginx_sp()
			print(bcolors.OKGREEN+'HTTP to HTTPS redirect has been forced for '+' '.join(app.get('domains'))+'.'+bcolors.ENDC)
		except:
			print(bcolors.OKGREEN+'HTTP to HTTPS redirect cannot be forced for '+' '.join(app.get('domains'))+'.'+bcolors.ENDC)
	else:
		print(bcolors.FAIL+'HTTP to HTTPS redirect cannot be enabled.'+bcolors.ENDC)

def disable_force_ssl(app):
	conf_file = app_custom_conf(app)
	if(conf_file and os.path.exists(conf_file)):
		try:
			os.unlink(conf_file)
			print(bcolors.OKBLUE+'HTTP to HTTPS redirect configuration file has been removed.'+bcolors.ENDC)
			print(bcolors.OKBLUE+'Reloading NGINX server...'+bcolors.ENDC)
			reload_nginx_sp()
			print(bcolors.OKGREEN+'HTTP to HTTPS redirection has been disabled for '+' '.join(app.get('domains'))+'.'+bcolors.ENDC)
		except:
			print(bcolors.FAIL+'HTTP to HTTPS redirection cannot be disabled for '+' '.join(app.get('domains'))+'.'+bcolors.ENDC)
	else:
		print(bcolors.HEADER+'HTTP to HTTPS redirection is not enabled for '+' '.join(app.get('domains'))+'.'+bcolors.ENDC)

def get_app_vhost(appname):
	return os.path.join(vhostsdir, appname+'.conf')

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def main():
	global apps
	ap = argparse.ArgumentParser(description='A Python script that automates the SSL installation on Ubuntu servers managed by ServerPilot.io.')
	ap.add_argument('-a', '--all', dest='all', help='Install SSL for all available apps.', action='store_const', const=True, default=False)
	ap.add_argument('-f', '--fresh', dest='fresh', help='Obtain and install SSL certificates for new (non-ssl) apps only.', action='store_const', const=True, default=False)
	ap.add_argument('-i', '--ignore', dest='ignoreapps', help='Comma-seperated app names to ignore some apps and install SSL for all others.', default=False)
	ap.add_argument('-n', '--name', dest='appname', help='Name of the app where SSL should be installed.', default=False)
	ap.add_argument('-r', '--renew', dest='renew', help='Renew all installed SSL certificates which are about to expire.', action='store_const', const=True, default=False)
	ap.add_argument('-ic', '--installcron', dest='installcron', help='Install the cron job for SSL renewals.', action='store_const', const=True, default=False)
	ap.add_argument('-dc', '--deletecron', dest='deletecron', help='Uninstall the cron job responsible for SSL renewals.', action='store_const', const=True, default=False)
	ap.add_argument('-ap', '--autopilot', dest='autopilot', help='A CRON job that attempts to automatically obtain SSL certificates for newly added apps.', action='store_const', const=True, default=False)
	ap.add_argument('-na', '--noautopilot', dest='noautopilot', help='Disable Autopilot mode and disable automatic SSLs for your apps.', action='store_const', const=True, default=False)
	ap.add_argument('-re', '--refresh', dest='refresh', help='Cleans all previous SSL vhost files, reinstalls the SSLs and reloads nginx. Only needed if you are having issues on a server with old SSL installations.', action='store_const', const=True, default=False)
	ap.add_argument('-redir', '--redirect', dest='redirect', help='Apply a 301 redirect from HTTP to HTTPs for a given app or for all apps.', default=False)
	ap.add_argument('-noredir', '--noredirect', dest='noredirect', help='Disable HTTP to HTTPs redirect for a single app or for all apps.', default=False)

	# Install certbo libs if not found
	do_initial_config()

	args = ap.parse_args()

	if(not os.path.isdir(vhostsdir)):
		print(bcolors.FAIL+'This package is intended to be used only on ServerPilot servers. Aborting!'+bcolors.ENDC)
		sys.exit()

	if args.all is True:
		apps = apps()
		for app in apps:
			do_final_ssl_install(app)

	elif args.appname:
		vhostfile = get_app_vhost(args.appname)
		app = get_app_info(vhostfile)
		if app:
			do_final_ssl_install(app)
		else:
			print(bcolors.FAIL+'Provided app name seems to be invalid as we did not find any vhost files for it.'+bcolors.ENDC)
	elif args.ignoreapps:
		apps = apps()
		ignoreapps = args.ignoreapps.split(',')
		print(bcolors.OKBLUE+str(len(ignoreapps))+' apps are being ignored.'+bcolors.ENDC)
		for app in apps:
			if app.get('appname') not in ignoreapps:
				do_final_ssl_install(app)
	elif args.renew is True:
		renew_ssls()
	elif args.installcron is True:
		install_sp_cron()
	elif args.deletecron is True:
		uninstall_sp_cron()
	elif args.fresh is True:
		sslstatus = ssl_status()
		nonsslapps = sslstatus.get('nonssl')
		if(len(nonsslapps) > 0):
			print(bcolors.OKBLUE+str(len(nonsslapps))+' non-ssl apps found for which SSL can be obtained. Proceeding...'+bcolors.ENDC)
			for nonssl in nonsslapps:
				do_final_ssl_install(nonssl)
		else:
			print(bcolors.OKBLUE+'We could not find any apps without SSL certificates installed.'+bcolors.ENDC)
	elif args.autopilot is True:
		add_autopilot_cron()
	elif args.noautopilot is True:
		disable_autopilot_cron()
	elif args.refresh is True:
		refresh_ssl_apps()
	elif args.redirect:
		if args.redirect == 'all':
			sslstatus = ssl_status()
			sslapps = sslstatus.get('ssl')
			if(len(sslapps) > 0):
				print(bcolors.HEADER+str(len(sslapps))+' SSL apps found for which HTTP to HTTPS redirect is being enabled.'+bcolors.ENDC)
				for app in sslapps:
					force_ssl(app)
		else:
			vhostfile = get_app_vhost(args.redirect)
			app = get_app_info(vhostfile)
			if app:
				if ssl_installed(app):
					force_ssl(app)
				else:
					print(bcolors.FAIL+'SSL is not installed for this app yet so redirect cannot be enabled.'+bcolors.ENDC)
			else:
				print(bcolors.FAIL+'Provided app name seems to be invalid as we did not find any vhost files for it.'+bcolors.ENDC)
	elif args.noredirect:
		if args.noredirect == 'all':
			apps = apps()
			for app in apps:
				disable_force_ssl(app)
		else:
			vhostfile = get_app_vhost(args.noredirect)
			app = get_app_info(vhostfile)
			if app:
				disable_force_ssl(app)
			else:
				print(bcolors.FAIL+'Provided app name seems to be invalid as we did not find any vhost files for it.'+bcolors.ENDC)

	else:
		ap.print_help()