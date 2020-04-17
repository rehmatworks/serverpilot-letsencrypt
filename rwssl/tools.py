import subprocess
import os
from jinja2 import Environment, BaseLoader
import pkgutil
import shutil
import pwd
import configparser
import warnings


def parsetpl(tpl, data={}):
    tplstr = str(pkgutil.get_data('rwssl', 'templates/{}'.format(tpl)).decode('utf-8'))
    tpl = Environment(loader=BaseLoader).from_string(tplstr)
    return tpl.render(**data)

def runcmd(cmd):
    FNULL = open(os.devnull, 'w')
    if not "sudo" in cmd:
        cmd = "sudo {}".format(cmd)
    subprocess.check_call([cmd], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

def reloadservice(service):
    runcmd('service {} reload'.format(service))

def restartservice(service):
    runcmd('service {} restart'.format(service))

def rmcontent(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

def getsubstr(s, start, end):
    return (s.split(start))[1].split(end)[0]

def userexists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

def doconfirm(msg = "Do you really want to perform this irreversible action"):
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("{} [Y/N] ".format(msg)).lower()
    return answer == "y"
