#!/usr/bin/python

#
# parser to provision qemu/libvirt VM from packer.io metadata
# sizing options (vCPU, vMem, vdd, network, VNC) in yaml-parameter file
# ./parser.py --config=config.yml --package=box.tgz
# ./parser.py -c config.yml -p box.tgz
#

# TODO: create program config file to define VM default values

import sys
import os.path
import getopt
import json
import yaml
import uuid
import tarfile
#from BeautifulSoup import BeautifulSoup
from lxml import etree
import ElementTree_pretty as ET_pretty

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

#TODO: load config dict from external file

config = { 'vm_files_path': "/opt/vm_images/",
           'os': {
               'type': {
                   'arch': 'x86_64',
                   'text': 'hvm'
                   },
               'boot': {
                   'dev': 'hd'
                   },
               },
           'devices': {
               'graphics': {
                   'type': 'vnc',
                   'port': '-1',
                   'keymap': 'en-us'
                   },
               'emulator': '/usr/libexec/qemu-kvm'
               }
         }

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
if os.path.exists(vm_package):
    tar = tarfile.open(vm_package)
    tar.extract("metadata.json")
    tar.close()
else:
    print("ERROR: vm-archive not found: %s" % vm_package )
    sys.exit()


# sanity-check metadata.json
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


# UUID is created dynamically by "virsh define"
#VM_UUID = uuid.uuid4()


#print("UUID: %s" % VM_UUID)
print("vdisk_size: %s" % vdisk_size)


# qemu-img convert image.qcow image.raw (defaults to convert to raw)
#call(["qemu-img", "convert" , "-p", "box_qcow.img", "box.raw"])

domain = etree.Element('domain', type='kvm')
doc = etree.ElementTree(domain)
os = etree.SubElement(domain, 'os')
os_type = etree.SubElement(os, 'type', arch=config['os']['type']['arch']).text=config['os']['type']['text']
os_boot = etree.SubElement(os, 'boot', dev=config['os']['boot']['dev'])

with open(vm_config_file, 'r') as stream:
    try:
        dict= (yaml.load(stream))
    except yaml.YAMLError as err:
        print(err)

if dict['name']:
    print("VM name:%s" % dict['name'])
    os = etree.SubElement(domain, 'name').text = dict['name']
else:
    print("Error: no VM name value found!")

if dict['cpu']:
    print("vCPU:%s" % dict['cpu'])
    vcpu = etree.SubElement(domain, 'vcpu').text = dict['cpu']
else:
    print("Error: no vCPU value found!")

if dict['mem']:
    print("vMem:%s" % dict['mem'])
    dict['mem_kb'] = int(dict['mem'])*1024*1024
    print("vMem_kb:%s kb" % dict['mem_kb'])
    memory = etree.SubElement(domain, 'memory').text = str(dict['mem_kb'])
else:
    print("Error: no vMem value found!")

devices = etree.SubElement(domain, 'devices')
graphics = etree.SubElement(devices, 'graphics', type=config['devices']['graphics']['type'], port=config['devices']['graphics']['port'], keymap=config['devices']['graphics']['keymap'])
emulator = etree.SubElement(devices, 'emulator').text=config['devices']['emulator']

if dict['disk']:
    for key, value in dict['disk'].iteritems():
        disk_file = etree.SubElement(devices, 'disk', device='disk', type='file')
        disk_src = etree.SubElement(disk_file, 'source', file=config['vm_files_path'] + value['source'])
        disk_tgt = etree.SubElement(disk_file, 'target', dev=value['target'])
        #print("disk name: %s file source:%s" % (key , value['source']))
        #print("disk name: %s disk target:%s" % (key , value['target']))
        
else:
    print("Error: no disk settings found!")

if dict['net']:
    for key, value in dict['net'].iteritems():
        devif = etree.SubElement(devices, 'interface', type='network')
        devif_src = etree.SubElement(devif, 'source', network=value['source_net'])
        devif_mac = etree.SubElement(devif, 'mac', address=value['mac'])
        #print("name: %s MAC:%s" % (key , value))
        print("name: %s net:%s" % (key , value['source_net']))
        print("name: %s mac:%s" % (key , value['mac']))
        
else:
    print("Error: no vNet settings found!")

print("Done yaml parsing")


print(ET_pretty.prettify(domain))
outFile3 = open('out3.xml', 'w')
xml_payload = ET_pretty.prettify(domain)
outFile3.write(xml_payload)
outFile3.close()
