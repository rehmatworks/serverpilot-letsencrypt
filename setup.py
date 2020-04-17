from setuptools import setup
import os
import subprocess
from setuptools.command.install import install

class SetupSslRenewCron(install):
	def run(self):
		crondir = '/etc/cron.weekly'
		cronfile = os.path.join(crondir, 'spsuite-sslrenewals')
		if not os.path.exists(crondir):
			os.makedirs(crondir)

		certbotpath = subprocess.check_output(['which', 'certbot']).strip().decode('utf8')
		with open(cronfile, 'w') as cf:
			cf.writelines(['#!/bin/sh\n', 'certbot renew --non-interactive --config-dir /etc/nginx-sp/le-ssls --post-hook "service nginx-sp reload"\n'])
		maxexeccmd = "chmod +x {}".format(cronfile)
		FNULL = open(os.devnull, 'w')
		subprocess.check_call([maxexeccmd], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
		install.run(self)

setup(name='spsuite',
	version='1.0.2',
	description='Command line utilities to manage ServerPilot provisioned servers.',
	author="Rehmat Alam",
	author_email="contact@rehmat.works",
	url="https://github.com/rehmatworks/spsuite",
	license="MIT",
	entry_points={
		'console_scripts': [
			'spsuite = spsuite.spsuite:main'
			],
	},
	packages=[
		'spsuite'
	],
	install_requires=[
		'python-nginx',
		'validators',
		'termcolor',
		'tabulate',
		'Jinja2',
		'pymysql',
		'certbot'
	],
	package_data={'spsuite':['templates/*.tpl']},
	cmdclass={
		'install': SetupSslRenewCron
	}
)
