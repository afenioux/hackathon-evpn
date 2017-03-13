#!/root/virtualenvs/junos/bin/python

# +-------------------------+
# |    v0.3 by Afenioux     |
# | ./deploy.py <username>  |
# | tested with python 2.7  |
# +-------------------------+

#
# used deploy the junos.conf configuration on equipement listed in sw_list.yml
# junos.conf should be a "static" file, no template in this example
#


from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import jnpr.junos.exception
from pprint import pprint
import yaml
import getpass
import sys

login = sys.argv[1]
pwd=getpass.getpass("passwd:")
comment="from PyEZ"
comment = raw_input("Type your commit comment:")


def make_rollback_and_quit(dev):
  cfg.rollback()
  cfg.unlock()
  print("\nrollback 0 done on " + dev.facts["hostname"])
  print("Exiting.")
  dev.close()
  exit()

f=open('sw_list.yml')
devices=yaml.load(f.read())

for host in devices:
  print("\n - - - - - -\n Proceeding with device : "+host)
  #dev=Device(host=host, user=login, password=pwd, gather_facts=False)
  dev=Device(host=host, user=login, password=pwd)
  try :
    dev.open()
  except jnpr.junos.exception.ConnectAuthError as error :
    print('\n Could not authenticate')
    exit()
  #pprint(dev.facts)
  cfg = Config(dev)
  # Execute Rollback to prevent commit change from old config session
  # We prefer to raise a LockError is config is not clean
  #cfg.rollback()
  try :
    cfg.lock() #ask for configure exclusive
  except jnpr.junos.exception.LockError as error :
    print('\nCould not set configure exclusive lock :')
    print(error.message)
    exit()
  try :
    cfg.load(path="junos.conf", format='set')
  except jnpr.junos.exception.ConfigLoadError as error :
    print('\nthere were some errors/warnings while loading the config :')
    print(error.message)
  print(cfg.pdiff())
  commit = raw_input("Commit? (y/N)")
  if commit in ["y", "Y", "Yes", "yes"]:
    try :
      cfg.commit(comment=comment)
      cfg.unlock()
      print ('configuration commited on ' + dev.facts["hostname"])
    except jnpr.junos.exception.CommitError as error :
      print('\ncommit failed on ' + dev.facts["hostname"])
      print('  ' + error.errs[0]['edit_path'])
      print('    ' + error.errs[0]['bad_element'])
      print(error.message)
      make_rollback_and_quit(dev)
  else:
    make_rollback_and_quit(dev)
