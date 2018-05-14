from setuptools import setup

setup(name='rwssl',
	version='1.0.0',
	description='ServerPilot Let\'s Encrypt SSL installation automation script.',
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