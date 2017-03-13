#!/usr/bin/env python

# +-------------------------+
# |    v0.1 by Afenioux     |
# | ./cli_run.py <username> |
# | tested with python 2.7  |
# +-------------------------+

#
# used to run a command on equipement listed in sw_list.yml
# for example : show firewall filter FILTER-NAME
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
command = raw_input("Type your full command (no all pipe commands implemented -display set is Ok-, no shortcut) : ")

f=open('sw_list.yml')
devices=yaml.load(f.read())

for host in devices:
  print("\n - - - - - -\n Proceeding with device : "+host)
  dev=Device(host=host, user=login, password=pwd)
  try :
    dev.open()
  except jnpr.junos.exception.ConnectAuthError as error :
    print('\n Could not authenticate')
    exit()
  #pprint(dev.facts)

  op = dev.cli(command, warning=False)
  data = [i for i in op.splitlines()]
  print '\n'.join(data)


