#!/usr/bin/python

#
# parser to provision qemu/libvirt VM from packer.io metadata
# sizing options (vCPU, vMem, vdd, network, VNC) in yaml-parameter file
# ./parser.py --config=config.yml --package=box.tgz
# ./parser.py -c config.yml -p box.tgz
#

import sys
import getopt
import json
import yaml
import uuid
import tarfile
from BeautifulSoup import BeautifulSoup
from subprocess import call


def usage():
    print("parser.py --config=<config.yml> --package=box.tgz")
    return


try:
    opts,args = getopt.getopt(sys.argv[1:], "hc:p:",["help","config=","package="])


except getopt.GetoptError as err:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)

vm_config_file = None
vm_package = None

for option, argument in opts:
    if option in ("-h", "--help"):
        usage()
        sys.exit()
    elif option in ("-c", "--config"):
        vm_config_file = argument
        print("config value: %s" % argument)
    elif option in ("-p", "--package"):
        vm_package = argument
        print("package value: %s" % argument)

if vm_config_file == None:
        usage()
        sys.exit()

if vm_package == None:
        usage()
        sys.exit()


# extract metadata.json from Packer build package
tar = tarfile.open(vm_package)
tar.extract("metadata.json")
tar.close()

# sanity-check etadata.json
with open('metadata.json') as packer_data:
    d = json.load(packer_data)

    if d['provider'] != "libvirt":
        print("ERROR: metadata.json provider != libvirt")

    if d['format'] != "qcow2":
        print("ERROR: metadata.json format != qcow2")

    if d['virtual_size']:
        vdisk_size = d['virtual_size']
    else:
        print("ERROR: metadata.json vdisk_size missing !")


VM_UUID = uuid.uuid4()


print("UUID: %s" % VM_UUID)
print("vdisk_size: %s" % vdisk_size)


# qemu-img convert image.qcow image.raw (defaults to convert to raw)
#call(["qemu-img", "convert" , "-p", "box_qcow.img", "box.raw"])

with open(vm_config_file, 'r') as stream:
    try:
        dict= (yaml.load(stream))
    except yaml.YAMLError as err:
        print(err)

if dict['name']:
    print("VM name:%s" % dict['name'])
else:
    print("Error: no VM name value found!")

if dict['cpu']:
    print("vCPU:%s" % dict['cpu'])
else:
    print("Error: no vCPU value found!")

if dict['mem']:
    print("vMem:%s" % dict['mem'])
    dict['mem_kb'] = int(dict['mem'])*1024*1024
    print("vMem_kb:%s kb" % dict['mem_kb'])
else:
    print("Error: no vMem value found!")

if dict['net']:

    for key, value in dict['net'].iteritems():
        print("vNet: %s MAC:%s" % (key , value))
else:
    print("Error: no vNet value found!")



with open("config.xml") as f:
        
        content = f.read()

        y = BeautifulSoup(content)
        print(y.domain.vcpu.contents[0])
        print(y.domain.devices.emulator.contents[0])
        tag = y.domain.vcpu
        tag.string.replaceWith(dict['cpu'])

        print(y.domain.vcpu.contents[0])

        tag_uuid = y.domain.uuid
        tag_uuid.string.replaceWith(str(VM_UUID))
        print(y.domain.uuid.contents[0])

        for tag in y.domain.devices.interface:
                print(tag)


soup = BeautifulSoup()
soup.append(soup.new_tag("a", href="http://www.example.com"))
print(soup)
