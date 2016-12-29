from fabric.api import run, env, roles, execute
from fabric.colors import red, green

#env.hosts = [ 'localhost', '127.0.0.1' ]

env.roledefs = {
    'db': ['localhost'],
    'web': ['127.0.0.1'],
}

def host_type():
    run('uname -a')

def diskfree():
    run('df -h')

def color_db():
  print(green("DB deployment GREEN") + red(" and some red characters...") + ".")

def color_web():
  print(red("WEB deployment in RED."))

# role-specific tasks
@roles('db')
def migrate():
    # Database stuff here.
    color_db()

@roles('web')
def update():
    # Code updates here.
    color_web()

# multi-host deployment script

def deploy():
    execute(migrate)
    execute(update)
