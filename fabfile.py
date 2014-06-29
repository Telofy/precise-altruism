# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from os.path import join, normpath
from fabric.api import env, run, cd

env.hosts = ['telofy@claviger.net']
env.base_dir = '~/precise-altruism'

def pull():
    with cd(env.base_dir):
        run('git pull')

def buildout(args=''):
    with cd(env.base_dir):
        run('test -a bin/buildout || python2.7 -S bootstrap.py')
        run('bin/buildout {}'.format(args))

def develop(args):
    with cd(env.base_dir):
        run('bin/develop {}'.format(args))

def circusd():
    with cd(env.base_dir):
        run('bin/circusd')

def start(process=''):
    with cd(env.base_dir):
        run('bin/circusctl start {}'.format(process))

def stop(process=''):
    with cd(env.base_dir):
        run('bin/circusctl stop {}'.format(process))

def restart(process=''):
    with cd(env.base_dir):
        run('bin/circusctl restart {}'.format(process))

def status():
    with cd(env.base_dir):
        run('bin/circusctl status')
