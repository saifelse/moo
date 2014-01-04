import os, sys, time
from tempfile import mkdtemp
from contextlib import contextmanager as _contextmanager

from fabric.api import cd, prefix, sudo, local, put, run
from fabric.api import env, task

env.site_path = '/srv/moo-site'
env.venv_path = '/srv/env'
env.user = 'pi'
env.hosts = ['moo.psyph.com']

@_contextmanager
def virtualenv():
  activate = 'source %s/bin/activate' % env.venv_path
  with prefix(activate):
    yield

@task
def stop():
  sudo('sv stop moo')

@task
def start():
  sudo('sv start moo')
  sudo('ln -sf /etc/nginx/sites-available/moo-www.conf /etc/nginx/sites-enabled/moo-www.conf')
  sudo('nginx -s reload')

def copy_project():
  tmp_folder = mkdtemp()
  tmp_file = os.path.join(tmp_folder, 'archive.tgz')
  copied_folder = "/srv/deploys/%s" % int(time.time())
  dest_file = os.path.join(copied_folder, 'archive.tgz')

  if sys.platform == 'darwin':  # brew install gnu-tar for OSX deployment
    local('gtar --exclude-vcs -czf %s .' % tmp_file)
  else:
    local('tar --exclude-vcs -czf %s .' % tmp_file)

  sudo('mkdir -p %s' % copied_folder)
  put(tmp_file, dest_file, use_sudo=True)

  with cd(copied_folder):
    sudo('tar -xvf %s .' % dest_file)

  sudo('ln -nsf %s %s' % (copied_folder, env.site_path))

def config_runit(name):
  sudo('rm -rf /etc/sv/%s' % name)
  sudo('rm -rf /etc/service/%s' % name)
  sudo('mkdir /etc/sv/%s -p' % name)

  sudo('cp config/run-%s /etc/sv/%s/run' % (name, name))
  sudo('chmod u+x /etc/sv/%s/run' % name)

  sudo('ln -s /etc/sv/%s /etc/service/%s' % (name, name))

@task
def bootstrap():
  # system updates
  sudo('apt-get update')

  # dependencies
  sudo('apt-get install python-dev python-virtualenv runit nginx -y')

  # create directory structure
  sudo('rm -rf /srv')
  sudo("chown %s /srv -R" % env.user)

  # setup virtualenvironment
  run('virtualenv %s' % env.venv_path)

  # start nginx
  sudo('sudo service nginx start')

  deploy()

@task
def deploy():
  # copy the project
  copy_project()

  # install project dependencies
  with cd(env.site_path):
    with virtualenv():
      run('pip install -r requirements.txt')

  # configure nginx
  with cd(env.site_path):
    sudo('cp -rf config/moo-www.conf /etc/nginx/sites-available/moo-www.conf')
    config_runit('moo')

  time.sleep(5)
  start()
