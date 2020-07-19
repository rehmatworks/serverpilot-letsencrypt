#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from .utils import ServerPilot
from termcolor import colored
import sys
import validators
from .tools import *
import shutil
import subprocess

def main():

    sp = ServerPilot()

    # Setup cron
    cronpath = '/etc/cron.weekly/rwssl-sslrenewals'
    if not os.path.exists(cronpath):
        croncmd = '%s renew --non-interactive --config-dir /etc/nginx-sp/le-ssls --post-hook "service nginx-sp reload"\n' % shutil.which('certbot')
        with open(cronpath, 'w') as cronfile:
            cronfile.write(cronfile.writelines(['#!/bin/sh\n', cmd]))
        maxexeccmd = "chmod +x {}".format(cronpath)
		FNULL = open(os.devnull, 'w')
		subprocess.check_call([maxexeccmd], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

    ap = argparse.ArgumentParser(description='A powerful tool to manage SSLs on servers provisioned using ServerPilot.io.')
    subparsers = ap.add_subparsers(dest="action")

    # SSL
    ssl = subparsers.add_parser('getcert', help='Get letsencrypt cert for an app.')
    ssl.add_argument('--app', dest='app', help='App name for which you want to get an SSL cert.', required=True)

    sslall = subparsers.add_parser('getcerts', help='Get letsencrypt certs for all apps.')
    sslall.add_argument('--user', dest='user', help='SSH user to activate SSL for their owned apps. If not provided, SSL will be activated for all apps.', required=False)

    ussl = subparsers.add_parser('removecert', help='Uninstall SSL cert from an app.')
    ussl.add_argument('--app', dest='app', help='App name from which you want to uninstall the SSL cert.', required=True)

    usslall = subparsers.add_parser('removecerts', help='Uninstall SSL certs for all apps.')
    usslall.add_argument('--user', dest='user', help='SSH user to remove SSLs for their owned apps. If not provided, SSL will be uninstalled from all apps.', required=False)

    forcessl = subparsers.add_parser('forcessl', help='Force SSL certificate for an app.')
    forcessl.add_argument('--app', dest='app', help='App name for which you want to force the HTTPS scheme.', required=True)

    unforcessl = subparsers.add_parser('unforcessl', help='Unforce SSL certificate for an app.')
    unforcessl.add_argument('--app', dest='app', help='App name for which you want to unforce the HTTPS scheme.', required=True)

    forceall = subparsers.add_parser('forceall', help='Force HTTPs for all apps.')
    forceall.add_argument('--user', dest='user', help='SSH user to force HTTPs for their owned apps. If not provided, SSL will be forced for all apps.', required=False)

    unforceall = subparsers.add_parser('unforceall', help='Unforce HTTPs for all apps.')
    unforceall.add_argument('--user', dest='user', help='SSH user to unforce HTTPs for their owned apps. If not provided, SSL will be unforced for all apps.', required=False)

    args = ap.parse_args()

    if len(sys.argv) <= 1:
        ap.print_help()
        sys.exit(0)

    if args.action == 'getcert':
        if doconfirm('Do you really want to obtain an SSL certificate for the app {}?'.format(args.app)):
            sp.setapp(args.app)
            try:
                print(colored('Activating SSL for app {}...'.format(args.app), 'blue'))
                sp.getcert()
            except Exception as e:
                print(colored(str(e), 'yellow'))

    if args.action == 'getcerts':
        if args.user:
            sp.setuser(args.user)
            confirmmsg = 'Do you really want to activate SSL for all apps owned by {}?'.format(args.user)
        else:
            confirmmsg = 'Do you really want to activate SSL for all apps existing on this server?'
        if doconfirm(confirmmsg):
            try:
                apps = sp.findapps()
                if len(apps) > 0:
                    for app in apps:
                        print(colored('Activating SSL for app {}...'.format(app[1]), 'blue'))
                        sp.app = app[1]
                        sp.getcert()
                else:
                    raise Exception('No apps found!')
            except Exception as e:
                print(colored(str(e), 'yellow'))

    if args.action == 'removecert':
        if doconfirm('Do you really want to uninstall SSL certificate for the app {}?'.format(args.app)):
            sp.setapp(args.app)
            try:
                print(colored('Uninstalling SSL from app {}...'.format(args.app), 'blue'))
                sp.removecert()
                print(colored('SSL has been uninstalled from the app {}.'.format(args.app), 'green'))
            except Exception as e:
                print(colored(str(e), 'yellow'))

    if args.action == 'removecerts':
        if args.user:
            sp.setuser(args.user)
            confirmmsg = 'Do you really want to uninstall SSL for all apps owned by {}?'.format(args.user)
        else:
            confirmmsg = 'Do you really want to uninstall SSL for all apps existing on this server?'
        if doconfirm(confirmmsg):
            try:
                apps = sp.findapps()
                if len(apps) > 0:
                    for app in apps:
                        print(colored('Removing SSL certificate from app {}...'.format(app[1]), 'blue'))
                        sp.app = app[1]
                        sp.removecert()
                        print(colored('SSL has been uninstalled from app {}.'.format(app[1]), 'green'))
                else:
                    raise Exception('No apps found!')
            except Exception as e:
                print(colored(str(e), 'yellow'))

    if args.action == 'forcessl':
        if doconfirm('Do you really want to force HTTPs for the app {}?'.format(args.app)):
            sp.setapp(args.app)
            try:
                sp.forcessl()
                print(colored('HTTPs has been forced for the app {}.'.format(args.app), 'green'))
            except Exception as e:
                print(colored(str(e), 'yellow'))

    if args.action == 'forceall':
        if args.user:
            sp.setuser(args.user)
            confirmmsg = 'Do you really want to force SSL for all apps owned by {}?'.format(args.user)
        else:
            confirmmsg = 'Do you really want to force SSL for all apps existing on this server?'
        if doconfirm(confirmmsg):
            try:
                apps = sp.findapps()
                if len(apps) > 0:
                    for app in apps:
                        print(colored('Forcing SSL certificate for app {}...'.format(app[1]), 'blue'))
                        try:
                            sp.app = app[1]
                            sp.forcessl()
                            print(colored('SSL has been forced for app {}.'.format(app[1]), 'green'))
                        except Exception as e:
                            print(colored(str(e), 'yellow'))
                else:
                    raise Exception('No apps found!')
            except Exception as e:
                print(colored(str(e), 'yellow'))

    if args.action == 'unforcessl':
        if doconfirm('Do you really want to unforce HTTPs for the app {}?'.format(args.app)):
            try:
                sp.setapp(args.app)
                sp.unforcessl()
                print(colored('HTTPs has been unforced for the app {}.'.format(args.app), 'green'))
            except Exception as e:
                print(colored(str(e), 'yellow'))

    if args.action == 'unforceall':
        if args.user:
            sp.setuser(args.user)
            confirmmsg = 'Do you really want to unforce SSL for all apps owned by {}?'.format(args.user)
        else:
            confirmmsg = 'Do you really want to unforce SSL for all apps existing on this server?'
        if doconfirm(confirmmsg):
            try:
                apps = sp.findapps()
                if len(apps) > 0:
                    for app in apps:
                        print(colored('Unforcing SSL certificate for app {}...'.format(app[1]), 'blue'))
                        try:
                            sp.app = app[1]
                            sp.unforcessl()
                            print(colored('SSL has been unforced for app {}.'.format(app[1]), 'green'))
                        except Exception as e:
                            print(colored(str(e), 'yellow'))
                else:
                    raise Exception('No apps found!')
            except Exception as e:
                print(colored(str(e), 'yellow'))
