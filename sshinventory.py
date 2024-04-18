import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()

ansibleRootPath=os.getenv('ANSIBLE_PATH')
sshConfigPath=os.getenv('SSH_CONFIG_PATH')

with open(ansibleRootPath+'ssh-inventory-json/nodes.json') as user_file:
  jsonfile = user_file.read()

data = json.loads(jsonfile)

sshConfigFile = sshConfigPath+"config"
#DELETE SSH CONFIG IF EXIST
if os.path.isfile(sshConfigFile):
      os.system("rm "+sshConfigFile)
#CREATE A NEW SSH CONFIG FILE
sshconfig = open(sshConfigFile, "a")

sshconfig.write("Host * \n")
sshconfig.write("   StrictHostKeyChecking accept-new \n\n")

inventoryFilePath = ansibleRootPath+"inventory"
#DELETE ANSIBLE INVENTORY IF EXIST
if os.path.isfile(inventoryFilePath):
      os.system("rm "+inventoryFilePath)
#CREATE A NEW ANSIBLE INVENTORY
inventoryFile = open(inventoryFilePath, "a")

inventoryFile.write("[ODOO]\n")

for cluster in data:
    for nodes in cluster:

        if not (nodes.get("nodename") is None ):
          sshconfig.write("#--------"+nodes["nodename"]+"----------------\n")

        if not (nodes.get("nodeproxy") is None ):
          sshconfig.write("Host "+nodes["nodeproxy"]+"\n")
          sshconfig.write("   HostName "+nodes["nodeproxy"]+"\n\n")

          for containers in nodes["data"]:
                  #ADD HOST ON ANSIBLE INVENTORY FILE
                  inventoryFile.write(containers["name"]+"\n")
                  #ADD HOST ON SSH CONFIG FILE
                  sshconfig.write("Host "+containers["name"]+"\n")
                  sshconfig.write("   HostName "+containers["ip"]+"\n")
                  sshconfig.write("   User root\n")
                  sshconfig.write("   ProxyJump "+nodes["nodeproxy"]+"\n\n")
        else:

          for containers in nodes["data"]:
                  #ADD HOST ON ANSIBLE INVENTORY FILE
                  inventoryFile.write(containers["name"]+"\n")
                  #ADD HOST ON SSH CONFIG FILE
                  sshconfig.write("Host "+containers["name"]+"\n")
                  sshconfig.write("   HostName "+containers["ip"]+"\n")
                  sshconfig.write("   User root\n")
        
sshconfig.close()