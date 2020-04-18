from setuptools import setup
import os
import subprocess
from setuptools.command.install import install
import shutil

import sys

sys.version_info < (3, 5)
	sys.exit('Error: rwssl only works in Python 3.x but you are using an older version')

class SetupSslRenewCron(install):
	def run(self):
		crondir = '/etc/cron.weekly'
		cronfile = os.path.join(crondir, 'rwssl-sslrenewals')
		if not os.path.exists(crondir):
			os.makedirs(crondir)
		cmd = '%s renew --non-interactive --config-dir /etc/nginx-sp/le-ssls --post-hook "service nginx-sp reload"\n' % shutil.which('certbot')
		with open(cronfile, 'w') as cf:
			cf.writelines(['#!/bin/sh\n', cmd])
		maxexeccmd = "chmod +x {}".format(cronfile)
		FNULL = open(os.devnull, 'w')
		subprocess.check_call([maxexeccmd], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
		install.run(self)

setup(name='rwssl',
	version='2.0.0',
	description='A Python package to manage Let\'s Encrypt SSL on ServerPilot provisioned servers.',
	author="Rehmat Alam",
	author_email="contact@rehmat.works",
	url="https://github.com/rehmatworks/serverpilot-letsencrypt/",
	license="MIT",
	entry_points={
		'console_scripts': [
			'rwssl = rwssl.rwssl:main'
			],
	},
	packages=[
		'rwssl'
	],
	install_requires=[
		'python-nginx',
		'validators',
		'termcolor',
		'tabulate',
		'Jinja2',
		'certbot'
	],
	package_data={'rwssl': ['templates/*.tpl']},
	cmdclass={
		'install': SetupSslRenewCron
	}
)
