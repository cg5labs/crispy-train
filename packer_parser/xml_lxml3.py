#!/usr/bin/python

from lxml import etree
import ElementTree_pretty as ET_pretty

# Create the root element
domain = etree.Element('domain')

# Make a new document tree
doc = etree.ElementTree(domain)

# Add the subelements
os = etree.SubElement(domain, 'os')
os_type = etree.SubElement(os, 'type', arch='x86_64').text='hvm'
devices = etree.SubElement(domain, 'devices')
dev_emulator = etree.SubElement(devices, 'emulator').text='/usr/bin/qemu-kvm'
dev_disk = etree.SubElement(devices, 'disk', type='file', device='disk')
dev_disk_driver = etree.SubElement(dev_disk, 'source', file='/opt/vm_images/centos-68.img')
dev_disk_driver = etree.SubElement(dev_disk, 'target', dev='hda')


disk1 = {
          'source': '/opt/vm_images/centos-68.img',
          'target': 'hda'
        }

disk2 = {
          'source': '/opt/vm_images/data.img',
          'target': 'hdb'
        }


disk_arr = [ disk1, disk2 ]

disk_arr2 = [ { 'source': '/opt/vm_images/centos-68.img', 'target': 'hda' }, { 'source': '/opt/vm_images/data.img', 'target': 'hdb' } ]

interface1 = { 'source_net': 'mgmt-dmz',
               'mac': '42:24'
             }

interface2 = { 'source_net': 'svc-dmz',
               'mac': '42:42'
             }

interface_arr = [ interface1, interface2 ]

interface_arr2 = [ { 'source_net': 'mgmt-dmz', 'mac': '42:24' }, { 'source_net': 'svc-dmz', 'mac': '12:24' }, ]


for interface in interface_arr2:
    devif = etree.SubElement(devices, 'interface', type='network')
    devif_src = etree.SubElement(devif, 'source', network=interface['source_net'])
    devif_mac = etree.SubElement(devif, 'mac', address=interface['mac'])

for disk in disk_arr2:
    disk_file = etree.SubElement(devices, 'disk', device='disk', type='file')
    disk_src = etree.SubElement(disk_file, 'source', file=disk['source'])
    disk_src = etree.SubElement(disk_file, 'target', dev=disk['target'])


# Save to XML file
print(ET_pretty.prettify(domain))

outFile2 = open('output2.xml', 'w')
xml_payload = ET_pretty.prettify(domain)
outFile2.write(xml_payload)


#outFile = open('output.xml', 'w')
#doc.write(outFile, xml_declaration=True, encoding='utf-16') 

#doc_pretty = (etree.tostring(domain, pretty_print=True))
#doc_pretty.write(oulFile2)
