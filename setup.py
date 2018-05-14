from setuptools import setup

setup(name='rwssl',
	version='3.0',
	description='ServerPilot Lets Encrypt SSL installation automation script.',
	author="Rehmat",
	author_email="contact@rehmat.works",
	url="https://github.com/rehmatworks/serverpilot-letsencrypt",
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
		'python-nginx'
	]
)